import json
import logging
import os
import time

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, text

from features.news.article_fetcher import fetch_article_text
from features.news.classifier import classify
from features.news.sources import fetch_all
from features.news.storage import save_news_items

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("news_runner")

# Free-tier Gemini is capped at a handful of requests per minute — this keeps
# us comfortably under that instead of burning through the quota in a burst.
SECONDS_BETWEEN_CLASSIFICATIONS = 7

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

UNCLASSIFIED_SQL = text(
    """
    SELECT id, title, url FROM news_items
    WHERE classified_at IS NULL
    ORDER BY fetched_at DESC
    LIMIT :limit
    """
)

UPDATE_CLASSIFICATION_SQL = text(
    """
    UPDATE news_items
    SET event = :event,
        assets = CAST(:assets AS JSONB),
        direction = :direction,
        importance = :importance,
        classified_at = now()
    WHERE id = :id
    """
)


def classify_pending(limit: int = 20):
    classified_count = 0
    with engine.begin() as conn:
        rows = conn.execute(UNCLASSIFIED_SQL, {"limit": limit}).fetchall()

        for i, row in enumerate(rows):
            item_id, title, url = row
            article_text = fetch_article_text(url)
            result = classify(title, article_text)

            if i < len(rows) - 1:
                time.sleep(SECONDS_BETWEEN_CLASSIFICATIONS)

            if result is None:
                continue

            conn.execute(
                UPDATE_CLASSIFICATION_SQL,
                {
                    "id": item_id,
                    "event": result.get("event"),
                    "assets": json.dumps(result.get("assets", [])),
                    "direction": result.get("direction"),
                    "importance": result.get("importance"),
                },
            )
            classified_count += 1

    return classified_count


def run():
    items = fetch_all()
    new_count = save_news_items(items)
    logger.info("fetched %d items, %d were new", len(items), new_count)

    classified = classify_pending()
    logger.info("classified %d pending items", classified)


if __name__ == "__main__":
    run()
