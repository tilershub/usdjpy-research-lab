from datetime import datetime, timezone
import json
import pandas as pd
import pytest
from research_context import Indicator, observation, transform_series, aligned_yield_spread, clean, recent_events
from economic_events import normalize_calendar
from newsfeed import parse_feed

NOW = datetime(2026,9,13,tzinfo=timezone.utc)
SPEC = Indicator('TEST','Test','US','economy','% YoY','Monthly',75,'Test','yoy')

def test_yoy_does_not_shift_over_missing_months():
    dates=pd.date_range('2024-01-01',periods=25,freq='MS')
    values=pd.Series(range(100,125),index=dates).drop(dates[12])
    got=transform_series(values,SPEC)
    assert dates[-1] not in got.index  # January 2025 denominator is absent.
    assert got.loc[dates[-2]] == pytest.approx((123/111-1)*100)

def test_stale_value_cannot_be_labelled_current():
    spec=Indicator('TEST','Test','JP','policy','%','Monthly',100,'Test')
    row=observation(spec,pd.Series([.25],index=pd.to_datetime(['2021-01-01'])),NOW)
    assert row['status']=='stale'
    assert row['released_at'] is None
    assert row['observed_at'].startswith('2021')

def test_future_and_infinite_observations_rejected():
    spec=Indicator('TEST','Test','US','policy','%','Daily',7,'Test')
    for dates, values in [(['2026-09-14'],[4.]),(['2026-09-12'],[float('inf')])]:
        assert observation(spec,pd.Series(values,index=pd.to_datetime(dates)),NOW)['status']=='unavailable'

def test_qoq_is_not_annualized():
    spec=Indicator('GDP','GDP','US','economy','% QoQ','Quarterly',200,'Test','qoq')
    values=pd.Series([100,102],index=pd.to_datetime(['2026-01-01','2026-04-01']))
    assert observation(spec,values,NOW)['value']==pytest.approx(2)

def test_spread_compares_only_matching_complete_months():
    us=pd.Series(4.,index=pd.bdate_range('2026-07-01','2026-09-10'))
    us.loc['2026-09-01':]=9.
    jp=pd.Series([1.,2.],index=pd.to_datetime(['2026-07-01','2026-09-01']))
    result=aligned_yield_spread({'DGS10':us,'IRLTLT01JPM156N':jp},NOW)
    assert result['value']==3
    assert result['observed_at'].startswith('2026-07')

def test_sparse_month_is_not_used_in_spread():
    us=pd.Series([5.],index=pd.to_datetime(['2026-08-01']))
    jp=pd.Series([1.],index=pd.to_datetime(['2026-08-01']))
    assert aligned_yield_spread({'DGS10':us,'IRLTLT01JPM156N':jp},NOW)['status']=='unavailable'

def test_calendar_preserves_zero_and_revision():
    frame=normalize_calendar([{'Country':'Japan','Date':'2026-09-12T00:00:00Z','Actual':0,'Forecast':0,'Previous':1,'Revised':'0.8','Unit':'%','SourceURL':'https://www.stat.go.jp/'}],NOW)
    row=recent_events(frame,NOW)[0]
    assert row['actual']==0 and row['forecast']==0
    assert row['revised']=='0.8'
    assert row['source_url']=='https://www.stat.go.jp/'

def test_rdf_headlines_supported():
    xml=b'<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/"><item><title>Decision</title><link>https://www.boj.or.jp/</link></item></rdf:RDF>'
    assert parse_feed(xml,'BOJ','JPY')[0]['headline']=='Decision'

def test_json_has_no_nan():
    assert json.dumps(clean({'value':float('nan')}),allow_nan=False)=='{"value": null}'
