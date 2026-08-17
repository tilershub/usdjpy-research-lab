from datetime import datetime, timezone

from policy_calendar import parse_calendar, upcoming

ROW = ('<div class="row fomc-meeting">'
       '<div class="fomc-meeting__month col-xs-5">{month}</div>'
       '<div class="fomc-meeting__date col-xs-4">{days}{marker}</div></div>')


def page(*years):
    parts = []
    for year, rows in years:
        parts.append(f"<h4>{year} FOMC Meetings</h4>")
        parts.extend(ROW.format(month=month, days=days, marker=marker) for month, days, marker in rows)
    return "".join(parts)


def test_two_day_meetings_resolve_to_the_decision_day():
    meetings = parse_calendar(page((2026, [("September", "15-16", "*"), ("October", "27-28", "")])))
    assert [m["date"] for m in meetings] == ["2026-09-16", "2026-10-28"]


def test_projection_meetings_are_flagged():
    meetings = parse_calendar(page((2026, [("September", "15-16", "*"), ("October", "27-28", "")])))
    assert meetings[0]["projections"] is True
    assert meetings[1]["projections"] is False


def test_single_day_meetings_are_supported():
    assert parse_calendar(page((2026, [("June", "17", "")])))[0]["date"] == "2026-06-17"


def test_a_meeting_spanning_two_months_uses_the_closing_month():
    assert parse_calendar(page((2026, [("Apr/May", "28-1", "")])))[0]["date"] == "2026-05-01"


def test_a_december_january_meeting_rolls_into_the_next_year():
    assert parse_calendar(page((2026, [("Dec/Jan", "31-1", "")])))[0]["date"] == "2027-01-01"


def test_meetings_are_deduplicated_and_ordered():
    html = page((2026, [("October", "27-28", "")]), (2025, [("January", "28-29", "")]))
    assert [m["date"] for m in parse_calendar(html)] == ["2025-01-29", "2026-10-28"]


def test_years_are_scoped_to_their_own_heading():
    html = page((2025, [("March", "18-19", "")]), (2026, [("March", "17-18", "")]))
    assert [m["date"] for m in parse_calendar(html)] == ["2025-03-19", "2026-03-18"]


def test_unparseable_markup_yields_nothing_rather_than_a_guess():
    assert parse_calendar("<div>no meetings here</div>") == []


def test_upcoming_skips_past_meetings_and_counts_days():
    meetings = parse_calendar(page((2026, [("September", "15-16", "*"), ("October", "27-28", "")])))
    ahead = upcoming(meetings, datetime(2026, 9, 20, tzinfo=timezone.utc))
    assert [m["date"] for m in ahead] == ["2026-10-28"]
    assert ahead[0]["days_away"] == 38
