"""Strict parser for the Statistics Bureau's published latest-indicator cards.

A missing/changed card fails closed. No release time or historical change is
inferred from this summary page. The original release remains linked.
"""
from datetime import datetime, timezone
import hashlib
from html import unescape
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin

URL='https://www.stat.go.jp/english/'
CARDS=[('JP_CPI','Consumer Price Index','Headline CPI inflation','% YoY','change over the year','/english/data/cpi/'),
       ('JP_UNEMPLOYMENT','Unemployment rate','Unemployment','%','seasonally adjusted','/english/data/roudou/')]


def parse_japan_statistics(html, now):
    rows=[]
    for id, heading, label, unit, qualifier, path in CARDS:
        row={'id':id,'label':label,'country':'JP','section':'economy','unit':unit,'frequency':'Monthly',
             'publisher':'Statistics Bureau of Japan','source_url':URL,'retrieved_at':now.isoformat(),
             'released_at':None,'status':'unavailable','value':None,'previous':None,'change':None,'history':[],
             'vintage':'Latest official summary; may be revised','note':'Official latest indicator. History and exact publication time are not supplied by this page.'}
        pattern=r'<a\b[^>]*href="('+re.escape(path)+r'[^"]*)"[^>]*>\s*'+re.escape(heading)+r'\s*<br\s*/?>\s*<span>\s*([-+]?\d+(?:\.\d+)?)\s*</span>\s*%\s*</a>\s*<div[^>]*>(.*?)</div>'
        matches=re.findall(pattern,html,re.S|re.I)
        if len(matches)==1:
            href,value,description=matches[0]
            plain=unescape(re.sub('<[^>]+>',' ',description))
            found=re.search(r'([A-Za-z]+)\s+(20\d{2})',plain)
            if qualifier in plain.lower() and found:
                try:
                    period=datetime.strptime(' '.join(found.groups()),'%B %Y').replace(tzinfo=timezone.utc)
                    age=(now-period).days
                    numeric=float(value)
                    if age>=0 and -100<numeric<100:
                        row.update(value=numeric,status='available' if age<=100 else 'stale',observed_at=period.isoformat(),age_days=age,
                                   source_url=urljoin(URL,href),source_page=URL,
                                   evidence_hash=hashlib.sha256((heading+value+plain).encode()).hexdigest())
                except ValueError: pass
        rows.append(row)
    return rows


def fetch_japan_statistics(now,timeout=20):
    try:
        with urlopen(Request(URL,headers={'User-Agent':'TRADE90-research/1.0'}),timeout=timeout) as response: html=response.read().decode('utf-8')
        return parse_japan_statistics(html,now)
    except Exception: return parse_japan_statistics('',now)
