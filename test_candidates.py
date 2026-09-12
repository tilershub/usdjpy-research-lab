import numpy as np
import pandas as pd
import pytest
from evaluate_candidates import dataset,evaluate,wilson


def prices(n=1200):
    return pd.Series(100*np.exp(np.random.default_rng(42).normal(0,.01,n).cumsum()),index=pd.bdate_range('2020-01-01',periods=n))


def test_features_do_not_change_when_future_prices_change():
    p=prices();a=dataset(p);q=p.copy();q.iloc[900:]*=2;b=dataset(q)
    cols=[c for c in a if c not in ('outcome','label_end')]
    pd.testing.assert_frame_equal(a.loc[:p.index[899],cols],b.loc[:p.index[899],cols])


def test_short_history_cannot_establish_target():
    with pytest.raises(ValueError):evaluate(prices(300))


def test_holdout_report_has_coverage_and_does_not_promote_small_sample():
    result,forecasts=evaluate(prices())
    assert result['target_validated'] is False
    assert result['all_forecasts']['observations']==len(forecasts)
    assert 0<=result['confidence_75_subset']['coverage']<=1
    assert (forecasts.label_end.iloc[:-1].to_numpy() <= forecasts.index[1:].to_numpy()+np.timedelta64(7,'D')).all()
    assert result['all_forecasts']['accuracy_95_interval'][0] <= result['all_forecasts']['accuracy']


def test_candidate_selection_does_not_use_final_holdout():
    p=prices();a,_=evaluate(p);q=p.copy();q.iloc[-150:]*=1.1;b,_=evaluate(q)
    assert a['selection_scores']==b['selection_scores']
    assert a['chosen']==b['chosen']
