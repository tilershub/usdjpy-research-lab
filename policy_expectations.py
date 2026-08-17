"""Market-implied Federal Reserve policy expectations.

Source: the Atlanta Fed's Market Probability Tracker, which fits probability
distributions to CME three-month SOFR options. It is the official, free, no-key
equivalent of the rate-probability tools traders quote, and unlike a scraped
FedWatch page it carries no licensing restriction.

The workbook is emitted with a broken drawing relationship that makes openpyxl
raise on load, so the sheet XML is read straight out of the zip container.
"""

from __future__ import annotations

import zipfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from io import BytesIO
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

MPT_URL = "https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/cenfis/market-probability-tracker/mpt_histdata.xlsx"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
EXCEL_EPOCH = date(1899, 12, 30)

CUT_FIELD = "Prob: cut"
HIKE_FIELD = "Prob: hike"
MEAN_FIELD = "Rate: mean"
MODE_FIELD = "Rate: mode"
WANTED_FIELDS = (CUT_FIELD, HIKE_FIELD, MEAN_FIELD, MODE_FIELD)


@dataclass(frozen=True)
class PolicyStatus:
    provider: str
    fetched_at: datetime
    cadence: str
    message: str = ""


def _cells(archive: zipfile.ZipFile, sheet: str, shared: list[str]):
    root = ET.fromstring(archive.read(sheet))
    for row in root.iter(f"{NS}row"):
        values = []
        for cell in row.iter(f"{NS}c"):
            kind = cell.get("t")
            if kind == "inlineStr":
                values.append("".join(node.text or "" for node in cell.iter(f"{NS}t")))
                continue
            node = cell.find(f"{NS}v")
            if node is None:
                values.append(None)
            elif kind == "s":
                values.append(shared[int(node.text)])
            else:
                values.append(node.text)
        yield values


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(f"{NS}t")) for si in root.iter(f"{NS}si")]


def _serial_to_date(value) -> date | None:
    try:
        return EXCEL_EPOCH + timedelta(days=int(float(value)))
    except (TypeError, ValueError):
        return None


def parse_workbook(payload: bytes) -> dict:
    """Return the most recent observation date's cut/hike odds by reference window."""
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        shared = _shared_strings(archive)
        rows = _cells(archive, "xl/worksheets/sheet3.xml", shared)
        header = next(rows, None)
        if not header or "date" not in [str(c).strip() for c in header if c]:
            raise ValueError("Market Probability Tracker workbook is missing its DATA header")
        latest_date = ""
        windows: dict[str, dict] = {}
        target_range = ""
        for observed, reference_start, current_range, field, value in (r[:5] for r in rows):
            if not observed or field not in WANTED_FIELDS:
                continue
            observed = str(observed).strip()
            if observed < latest_date:
                continue
            if observed > latest_date:
                latest_date, windows, target_range = observed, {}, ""
            target_range = str(current_range or "").strip() or target_range
            window = _serial_to_date(reference_start)
            if window is None:
                continue
            try:
                numeric = float(str(value).strip())
            except ValueError:
                continue
            windows.setdefault(window.isoformat(), {})[field] = numeric
    if not latest_date:
        raise ValueError("Market Probability Tracker workbook contained no usable observations")
    return {"observed": latest_date, "target_range": target_range, "windows": windows}


def _summarise(parsed: dict, horizons: int = 4) -> dict:
    ordered = sorted(parsed["windows"].items())[:horizons]
    outlook = []
    for window, fields in ordered:
        cut = fields.get(CUT_FIELD)
        hike = fields.get(HIKE_FIELD)
        hold = None if cut is None or hike is None else max(0.0, round(100.0 - cut - hike, 2))
        outlook.append({
            "reference_start": window,
            "cut_probability": cut,
            "hold_probability": hold,
            "hike_probability": hike,
            "expected_rate_bps": fields.get(MEAN_FIELD),
            "modal_rate_bps": fields.get(MODE_FIELD),
        })
    return {
        "observed": parsed["observed"],
        "target_range": parsed["target_range"],
        "outlook": outlook,
        "next_meeting_bias": _bias(outlook[0]) if outlook else "Unknown",
    }


def _bias(window: dict) -> str:
    cut, hike = window.get("cut_probability"), window.get("hike_probability")
    if cut is None or hike is None:
        return "Unknown"
    if cut >= 60:
        return "Easing priced"
    if hike >= 60:
        return "Tightening priced"
    if max(cut, hike) < 40:
        return "Hold priced"
    return "Easing leaning" if cut > hike else "Tightening leaning"


def fetch_policy_expectations(timeout: int = 60) -> tuple[dict, PolicyStatus]:
    now = datetime.now(timezone.utc)
    provider = "Atlanta Fed Market Probability Tracker"
    cadence = "Business daily, derived from CME 3-month SOFR options"
    request = Request(MPT_URL, headers={"User-Agent": "TRADE90-research/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = response.read()
        return _summarise(parse_workbook(payload)), PolicyStatus(provider, now, cadence)
    except Exception as exc:
        return {}, PolicyStatus(provider, now, cadence, f"Policy expectations unavailable: {exc}")
