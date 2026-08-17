import io
import zipfile
from datetime import date

import pytest

from policy_expectations import EXCEL_EPOCH, _bias, _summarise, parse_workbook

SHEET = """<?xml version="1.0"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
<row><c t="inlineStr"><is><t>date</t></is></c><c t="inlineStr"><is><t>reference_start</t></is></c><c t="inlineStr"><is><t>target_range</t></is></c><c t="inlineStr"><is><t>field</t></is></c><c t="inlineStr"><is><t>value</t></is></c></row>
{rows}
</sheetData></worksheet>"""

ROW = ('<row><c t="inlineStr"><is><t>{observed}</t></is></c><c><v>{serial}</v></c>'
       '<c t="inlineStr"><is><t>{target}</t></is></c>'
       '<c t="inlineStr"><is><t>{field}</t></is></c><c t="inlineStr"><is><t>{value}</t></is></c></row>')

SEPT_WINDOW = date(2026, 9, 16)
SEPT_SERIAL = (SEPT_WINDOW - EXCEL_EPOCH).days


def workbook(rows):
    body = "\n".join(ROW.format(**row) for row in rows)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("xl/worksheets/sheet3.xml", SHEET.format(rows=body))
    return buffer.getvalue()


def rows_for(observed, serial=SEPT_SERIAL, target="350bps - 375bps", cut="10.0", hike="20.0"):
    return [
        {"observed": observed, "serial": serial, "target": target, "field": "Prob: cut", "value": cut},
        {"observed": observed, "serial": serial, "target": target, "field": "Prob: hike", "value": hike},
        {"observed": observed, "serial": serial, "target": target, "field": "Rate: mean", "value": "378.5"},
    ]


def test_only_the_most_recent_observation_date_is_used():
    payload = workbook(rows_for("2026-08-10", cut="80.0", hike="5.0") + rows_for("2026-08-14"))
    parsed = parse_workbook(payload)
    assert parsed["observed"] == "2026-08-14"
    assert parsed["windows"]["2026-09-16"]["Prob: cut"] == 10.0


def test_excel_serial_dates_resolve_to_the_reference_window():
    parsed = parse_workbook(workbook(rows_for("2026-08-14")))
    assert _summarise(parsed)["outlook"][0]["reference_start"] == "2026-09-16"


def test_hold_probability_is_the_residual_and_never_negative():
    parsed = parse_workbook(workbook(rows_for("2026-08-14", cut="10.0", hike="20.0")))
    assert _summarise(parsed)["outlook"][0]["hold_probability"] == 70.0

    parsed = parse_workbook(workbook(rows_for("2026-08-14", cut="70.0", hike="60.0")))
    assert _summarise(parsed)["outlook"][0]["hold_probability"] == 0.0


def test_a_workbook_without_observations_fails_rather_than_guessing():
    with pytest.raises(ValueError):
        parse_workbook(workbook([]))


@pytest.mark.parametrize("cut, hike, expected", [
    (75.0, 1.0, "Easing priced"),
    (1.0, 75.0, "Tightening priced"),
    (10.0, 20.0, "Hold priced"),
    (45.0, 40.0, "Easing leaning"),
    (40.0, 45.0, "Tightening leaning"),
    (None, 45.0, "Unknown"),
])
def test_bias_labels_follow_the_priced_probabilities(cut, hike, expected):
    assert _bias({"cut_probability": cut, "hike_probability": hike}) == expected
