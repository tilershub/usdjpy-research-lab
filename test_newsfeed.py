from newsfeed import BROAD_MARKET_ASSETS, news_for_pair, parse_feed

FEED = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
<item><title>Older statement</title><link>https://example.invalid/a</link><pubDate>Mon, 10 Aug 2026 12:00:00 GMT</pubDate></item>
<item><title>Latest decision</title><link>https://example.invalid/b</link><pubDate>Fri, 14 Aug 2026 18:30:00 GMT</pubDate></item>
<item><link>https://example.invalid/untitled</link><pubDate>Fri, 14 Aug 2026 19:00:00 GMT</pubDate></item>
</channel></rss>"""


def test_entries_are_newest_first_and_untitled_items_are_dropped():
    entries = parse_feed(FEED, "Federal Reserve", "USD")
    assert [entry["headline"] for entry in entries] == ["Latest decision", "Older statement"]
    assert entries[0]["published_at"].startswith("2026-08-14T18:30")
    assert entries[0]["currency"] == "USD"


def test_limit_is_respected():
    assert len(parse_feed(FEED, "Federal Reserve", "USD", limit=1)) == 1


def test_pair_relevance_matches_the_currencies_that_set_policy():
    entries = [
        {"currency": "USD", "headline": "a", "source": "Federal Reserve", "url": "", "published_at": "2026-08-14"},
        {"currency": "EUR", "headline": "b", "source": "European Central Bank", "url": "", "published_at": "2026-08-13"},
    ]
    assert {e["currency"] for e in news_for_pair(entries, "EUR", "USD")} == {"EUR", "USD"}
    assert [e["currency"] for e in news_for_pair(entries, "JPY", "USD")] == ["USD"]


def test_gold_and_bitcoin_take_every_central_bank_release():
    entries = [
        {"currency": "USD", "headline": "a", "source": "Federal Reserve", "url": "", "published_at": "2026-08-14"},
        {"currency": "EUR", "headline": "b", "source": "European Central Bank", "url": "", "published_at": "2026-08-13"},
    ]
    for asset in BROAD_MARKET_ASSETS:
        assert len(news_for_pair(entries, asset, "USD")) == 2
