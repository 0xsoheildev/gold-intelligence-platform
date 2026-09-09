import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

INSERT_NEWS_SQL = text(
    """
    INSERT INTO news_items (source, title, url, summary, published_at)
    VALUES (:source, :title, :url, :summary, :published_at)
    ON CONFLICT (url) DO NOTHING
    """
)


def save_news_items(items) -> int:
    """Returns how many were actually new (ON CONFLICT means re-fetched duplicates are silently skipped)."""
    if not items:
        return 0

    inserted = 0
    with engine.begin() as conn:
        for item in items:
            result = conn.execute(
                INSERT_NEWS_SQL,
                {
                    "source": item.source,
                    "title": item.title,
                    "url": item.url,
                    "summary": item.summary,
                    "published_at": item.published_at,
                },
            )
            inserted += result.rowcount
    return inserted
