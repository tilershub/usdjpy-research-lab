import pytest
from retail_sentiment import normalize_retail, fetch_retail

def test_rejects_bad_percentages_and_retains_sample_basis():
    rows=normalize_retail({'error':False,'symbols':[{'name':'USDJPY','longPercentage':70,'shortPercentage':30},{'name':'BAD','longPercentage':float('nan'),'shortPercentage':30}]})
    assert len(rows)==1 and rows[0]['long_percent']==70
    assert 'Provider' in rows[0]['basis']

def test_provider_failure_not_empty_success():
    with pytest.raises(ValueError): normalize_retail({'error':True,'symbols':[]})

def test_no_access_does_not_make_request(monkeypatch):
    monkeypatch.delenv('MYFXBOOK_SESSION',raising=False)
    assert fetch_retail()['status']=='Credentials and display permission required'
