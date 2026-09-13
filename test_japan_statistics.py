from datetime import datetime,timezone
from japan_statistics import parse_japan_statistics
NOW=datetime(2026,9,13,tzinfo=timezone.utc)
HTML='<a href="/english/data/cpi/1581-z.html">Consumer Price Index<br><span>1.9</span>%</a><div>July 2026<br>change over the year</div>'
def test_official_card_retains_date_and_basis():
 row=parse_japan_statistics(HTML,NOW)[0]
 assert row['value']==1.9 and row['unit']=='% YoY'
 assert row['observed_at'].startswith('2026-07')
 assert row['released_at'] is None and row['change'] is None
 assert row['status']=='available'
def test_changed_definition_and_future_date_fail_closed():
 for html in [HTML.replace('over the year','over the month'), HTML.replace('July 2026','July 2027'),HTML+HTML,'']:
  assert parse_japan_statistics(html,NOW)[0]['status']=='unavailable'
