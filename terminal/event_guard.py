"""Official BLS release-aware safety context for delayed TRADE90 research.

This is NOT a comprehensive economic calendar or market reaction feed. Events
from the official schedule invalidate any implication that the daily model is a
current intraday recommendation. We never infer price reaction from macro data.
"""
import re
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from django.core.cache import cache

BLS_ICS_URL = "https://www.bls.gov/schedule/news_release/bls.ics"
BLS_CPI_SCHEDULE = "https://www.bls.gov/schedule/news_release/cpi.htm"
BLS_CPI_2026_10 = "https://www.bls.gov/news.release/archives/cpi_10142026.htm"
UTC = timezone.utc
ET = ZoneInfo("America/New_York")

# Verified published dates for CPI from BLS's official release schedule.
# Fallback protects traders if a live government calendar is unreachable; it
# must never be construed as a complete BLS calendar.
VERIFIED_CPI_FALLBACK = (
    ("2026-10-14T08:30:00", "Consumer Price Index"),
    ("2026-11-10T08:30:00", "Consumer Price Index"),
    ("2026-12-10T08:30:00", "Consumer Price Index"),
)
CRITICAL = ("consumer price index", "employment situation", "producer price index")


def _ics_datetime(row):
    match = re.match(r"^DTSTART(?:;([^:]+))?:(\d{8}(?:T\d{4}(?:\d{2})?Z?)?)$", row)
    if not match:
        return None
    attrs, raw = match.groups()
    if "T" not in raw:
        return None  # All-day event is not sufficient to time a risk window.
    is_utc = raw.endswith("Z")
    data = raw.rstrip("Z")
    try:
        dt = datetime.strptime(data, "%Y%m%dT%H%M%S" if len(data) == 15 else "%Y%m%dT%H%M")
    except ValueError:
        return None
    if is_utc:
        return dt.replace(tzinfo=UTC)
    zone = ET
    if attrs and "TZID=" in attrs:
        tz = attrs.split("TZID=", 1)[1].split(";", 1)[0]
        try:
            zone = ZoneInfo(tz)
        except Exception:
            return None
    return dt.replace(tzinfo=zone).astimezone(UTC)


def parse_official_ical(text):
    """Parse a tightly limited subset of official BLS iCalendar VEVENT."""
    if not isinstance(text, str) or len(text) > 1_000_000:
        return []
    unfolded = re.sub(r"\r?\n[ \t]", "", text)
    out = []
    for record in unfolded.split("BEGIN:VEVENT")[1:]:
        record = record.split("END:VEVENT", 1)[0]
        lines = record.splitlines()
        title = next((line.split(":", 1)[1].strip() for line in lines
                      if line.startswith("SUMMARY:") and ":" in line), "")
        if not any(term in title.lower() for term in CRITICAL):
            continue
        stamp = next((_ics_datetime(line.strip()) for line in lines
                      if line.startswith("DTSTART") and _ics_datetime(line.strip())), None)
        if stamp:
            out.append({"name": title[:90], "scheduled_at": stamp.isoformat(),
                        "url": BLS_ICS_URL, "source": "U.S. Bureau of Labor Statistics official calendar"})
    return out


def get_bls_scheduled():
    cached = cache.get("trade90:bls:highimpact:2026-v1")
    if cached is not None:
        return cached
    events = []
    try:
        req = Request(BLS_ICS_URL, headers={"User-Agent": "TRADE90 research/1.0", "Accept": "text/calendar"})
        with urlopen(req, timeout=4) as response:
            raw = response.read(1_000_001)
            if len(raw) > 1_000_000:
                raise ValueError("BLS calendar exceeds permitted size")
        events = parse_official_ical(raw.decode("utf-8"))
    except (OSError, ValueError, HTTPError, URLError, UnicodeError):
        pass
    fallback = [{"name": name, "scheduled_at": datetime.fromisoformat(iso).replace(tzinfo=ET).astimezone(UTC).isoformat(),
                 "url": BLS_CPI_SCHEDULE, "source": "Verified BLS CPI schedule"}
                for iso, name in VERIFIED_CPI_FALLBACK]
    had_live_calendar = bool(events)
    known = {(e["scheduled_at"], e["name"].lower()) for e in events}
    # Official verified CPI date protection must work even if the ICS feed
    # omits or abbreviates a particular CPI event.
    for fallback_event in fallback:
        same_time = any(x["scheduled_at"] == fallback_event["scheduled_at"] and
                        "consumer price" in x["name"].lower() for x in events)
        if not same_time:
            events.append(fallback_event)
    source_status = ("official BLS iCalendar plus verified CPI dates; excludes Fed/other-country events"
                     if had_live_calendar else
                     "limited verified BLS CPI schedule fallback; other high-impact events unverified")
    value = {"events": events, "source_status": source_status}
    cache.set("trade90:bls:highimpact:2026-v1", value, 900)
    return value


def recent_high_impact(now=None):
    now = now or datetime.now(UTC)
    scheduled = get_bls_scheduled()
    candidates = []
    for event in scheduled["events"]:
        try:
            t = datetime.fromisoformat(event["scheduled_at"]).astimezone(UTC)
        except (ValueError, TypeError):
            continue
        hours = (now - t).total_seconds() / 3600
        if -24 <= hours <= 36:
            candidates.append((abs(hours), hours, event))
    if not candidates:
        return {"status": "unknown", "source_status": scheduled["source_status"],
                "message": "No verified release window from the limited BLS feed. Economic risk is NOT cleared."}
    _, hours, source = min(candidates)
    stage = "upcoming" if hours < 0 else "released_or_due"
    result = {"status": stage, "name": source["name"],
              "scheduled_at": source["scheduled_at"], "source": source["source"],
              "url": source["url"], "hours_from_release": round(hours, 1),
              "source_status": scheduled["source_status"],
              "message": ("Official high-impact U.S. data scheduled soon; existing research is pre-event."
                          if hours < 0 else
                          "High-impact U.S. release window passed. Do not rely on a pre-event model bias.")}
    # Narrow, dated editorial source note from the BLS primary release. This is
    # not a live price reaction and explicitly expires after 36 hours.
    cpi_at = datetime(2026, 10, 14, 12, 30, tzinfo=UTC)
    if "consumer price index" in source["name"].lower() and abs((t - cpi_at).total_seconds()) < 60 and hours >= 0:
        result["official_release"] = {
            "headline": "U.S. CPI for September 2026 (official BLS release)",
            "headline_yoy_pct": 3.7, "headline_mom_pct": 0.6,
            "core_yoy_pct": 2.6, "core_mom_pct": 0.3,
            "source": "U.S. Bureau of Labor Statistics, October 14, 2026",
            "source_url": BLS_CPI_2026_10,
            "note": "Verified macro figures only. No assumption about current Gold, EUR/USD or USD/JPY prices."
        }
    return result
