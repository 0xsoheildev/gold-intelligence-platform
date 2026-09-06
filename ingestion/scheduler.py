"""
Phase 1 Scheduler — Fetches the sources every 10 minutes and stores the data in `raw_prices`.**

**Run:**

python -m ingestion.scheduler

"""

import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler

from ingestion.db import save_price_points
from ingestion.sources.goldapi_source import GoldApiSource
from ingestion.sources.tgju_source import TgjuSource

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("scheduler")

FETCH_INTERVAL_MINUTES = int(os.environ.get("FETCH_INTERVAL_MINUTES", "10"))

sources = [
    TgjuSource(),
    GoldApiSource(api_key=os.environ.get("GOLDAPI_KEY", "")),
]


def run_fetch_cycle():
    for source in sources:
        try:
            points = source.fetch()
            saved = save_price_points(points)
            logger.info("منبع %s: %d قیمت ذخیره شد", source.name, saved)
        except Exception:
            logger.exception("خطا در fetch از منبع %s", source.name)


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_fetch_cycle, "interval", minutes=FETCH_INTERVAL_MINUTES)

    logger.info("شروع scheduler — هر %d دقیقه اجرا می‌شه", FETCH_INTERVAL_MINUTES)
    run_fetch_cycle()
    scheduler.start()
