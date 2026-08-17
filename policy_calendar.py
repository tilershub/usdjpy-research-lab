"""FOMC meeting schedule, published by the Federal Reserve itself.

The general-purpose calendar provider this project used was retired, and the
free replacements either need a key or redistribute someone else's licensed
feed. Meeting dates are different: the Fed publishes its own schedule years
ahead, so the single highest-impact scheduled event for gold and the dollar can
be read from the primary source with no key and no licence.

This deliberately covers FOMC meetings only. It is not a general economic
calendar and does not pretend to be one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from urllib.request import Request, urlopen

FOMC_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"

YEAR_HEADING = re.compile(r"(20\d\d)\s+FOMC Meetings")
MEETING_ROW = re.compile(
    r'fomc-meeting__month[^>]*>\s*(?:<strong>)?\s*([A-Za-z]+(?:/[A-Za-z]+)?)\s*(?:</strong>)?\s*</div>'
    r'.*?fomc-meeting__date[^>]*>\s*(?:<strong>)?\s*([0-9]{1,2}(?:-[0-9]{1,2})?)\s*(\*?)',
    re.DOTALL,
)
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


@dataclass(frozen=True)
class CalendarStatus:
    provider: str
    fetched_at: datetime
    cadence: str
    message: str = ""


def _decision_day(month_text: str, day_text: str, year: int) -> date | None:
    """Two-day meetings decide on the second day, which may fall in the next month."""
    months = [MONTHS.get(part.strip().lower()) for part in month_text.split("/")]
    months = [m for m in months if m]
    days = [int(part) for part in day_text.split("-") if part]
    if not months or not days:
        return None
    month = months[-1]
    day = days[-1]
    # "Jan/Feb" with "31-1" rolls into the following year only when it wraps December.
    rollover = year + 1 if months[0] == 12 and month < months[0] else year
    try:
        return date(rollover, month, day)
    except ValueError:
        return None


def parse_calendar(html: str) -> list[dict]:
    meetings = []
    headings = list(YEAR_HEADING.finditer(html))
    for index, heading in enumerate(headings):
        year = int(heading.group(1))
        end = headings[index + 1].start() if index + 1 < len(headings) else len(html)
        segment = html[heading.end():end]
        for month_text, day_text, marker in MEETING_ROW.findall(segment):
            decision = _decision_day(month_text, day_text, year)
            if decision is None:
                continue
            meetings.append({
                "date": decision.isoformat(),
                "label": f"FOMC decision ({month_text} {day_text})",
                "projections": marker == "*",
            })
    unique = {meeting["date"]: meeting for meeting in meetings}
    return [unique[key] for key in sorted(unique)]


def upcoming(meetings: list[dict], now: datetime | None = None, limit: int = 4) -> list[dict]:
    today = (now or datetime.now(timezone.utc)).date()
    future = []
    for meeting in meetings:
        when = date.fromisoformat(meeting["date"])
        if when < today:
            continue
        future.append({**meeting, "days_away": (when - today).days})
    return future[:limit]


def fetch_fomc_calendar(timeout: int = 30) -> tuple[list[dict], CalendarStatus]:
    now = datetime.now(timezone.utc)
    provider = "Federal Reserve FOMC meeting calendar"
    cadence = "Published years ahead; decision days only"
    request = Request(FOMC_URL, headers={"User-Agent": "TRADE90-research/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="replace")
        meetings = parse_calendar(html)
        if not meetings:
            raise ValueError("FOMC calendar page contained no recognisable meeting rows")
        return meetings, CalendarStatus(provider, now, cadence)
    except Exception as exc:
        return [], CalendarStatus(provider, now, cadence, f"FOMC calendar unavailable: {exc}")
