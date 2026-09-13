"""Optional Myfxbook adapter. Session stays server-side; no login/password storage."""
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import math


def normalize_retail(payload):
    if payload.get('error') is not False or not isinstance(payload.get('symbols'), list):
        raise ValueError('Invalid provider response')
    rows=[]
    for row in payload['symbols']:
        try:
            long, short = float(row['longPercentage']), float(row['shortPercentage'])
            if not all(math.isfinite(x) and 0 <= x <= 100 for x in (long, short)) or abs(long+short-100)>2:
                continue
            rows.append({'symbol': str(row['name']).upper(), 'long_percent': long, 'short_percent': short,
                         'basis': 'Provider-reported percentages; do not combine with account-count measures.'})
        except (KeyError, TypeError, ValueError):
            continue
    return rows


def fetch_retail(timeout=12):
    result={'provider': 'Myfxbook', 'source_url': 'https://www.myfxbook.com/community/outlook',
            'retrieved_at': datetime.now(timezone.utc).isoformat(), 'observed_at': None,
            'status': 'Credentials and display permission required', 'rows': [],
            'note': 'Provider sample only. Retrieval time is not the position observation time. No contrarian signal.'}
    session = os.getenv('MYFXBOOK_SESSION')
    if not session or os.getenv('MYFXBOOK_DISPLAY_ALLOWED') != 'true':
        return result
    try:
        url = 'https://www.myfxbook.com/api/get-community-outlook.json?'+urlencode({'session': session})
        with urlopen(Request(url, headers={'User-Agent': 'TRADE90-research/1.0'}),timeout=timeout) as response:
            rows=normalize_retail(json.load(response))
        return {**result, 'status': 'Provider timestamp unavailable' if rows else 'Unavailable', 'rows': rows}
    except Exception:
        return {**result, 'status': 'Unavailable'}
