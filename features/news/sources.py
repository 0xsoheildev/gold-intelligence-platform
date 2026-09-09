from dataclasses import dataclass
from datetime import datetime, timezone

import feedparser

# investing.com uses numeric feed IDs per category — these were verified working:
# news_11 = commodities (gold, oil, silver, copper), news_1 = forex (dollar, rate
# expectations) — both directly relevant to gold price drivers.
FEEDS = {
    "investing_commodities": "https://www.investing.com/rss/news_11.rss",
    "investing_forex": "https://www.investing.com/rss/news_1.rss",
}


@dataclass
class NewsItem:
    source: str
    title: str
    url: str
    summary: str
    published_at: datetime | None


def _parse_published(entry) -> datetime | None:
    parsed = getattr(entry, "published_parsed", None)
    if not parsed:
        return None
    return datetime(*parsed[:6], tzinfo=timezone.utc)


def fetch_feed(source_name: str, feed_url: str) -> list[NewsItem]:
    parsed = feedparser.parse(feed_url)
    return [
        NewsItem(
            source=source_name,
            title=entry.get("title", "").strip(),
            url=entry.get("link", "").strip(),
            summary=entry.get("summary", "").strip(),
            published_at=_parse_published(entry),
        )
        for entry in parsed.entries
        if entry.get("link")
    ]


def fetch_all() -> list[NewsItem]:
    items: list[NewsItem] = []
    for name, url in FEEDS.items():
        try:
            items.extend(fetch_feed(name, url))
        except Exception:
            # one dead/changed feed shouldn't block the others
            continue
    return items
