import logging
import os

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, text

from features.quality.consensus import consensus_price
from features.quality.detector import detect_outliers
from features.quality.reliability import update_reliability

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("quality_runner")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

DISTINCT_SYMBOLS_SQL = text("SELECT DISTINCT symbol FROM raw_prices")

LATEST_PER_SOURCE_SQL = text(
    """
    SELECT DISTINCT ON (source) source, price, currency
    FROM raw_prices
    WHERE symbol = :symbol
    ORDER BY source, fetched_at DESC
    """
)

GET_RELIABILITY_SQL = text("SELECT reliability FROM source_reliability WHERE source = :source")

UPSERT_RELIABILITY_SQL = text(
    """
    INSERT INTO source_reliability (source, reliability, updated_at)
    VALUES (:source, :reliability, now())
    ON CONFLICT (source) DO UPDATE SET reliability = :reliability, updated_at = now()
    """
)

INSERT_CONSENSUS_SQL = text(
    """
    INSERT INTO consensus_prices (symbol, price, currency, method)
    VALUES (:symbol, :price, :currency, 'reliability_weighted')
    """
)


def _get_reliability(conn, source: str) -> float:
    row = conn.execute(GET_RELIABILITY_SQL, {"source": source}).fetchone()
    return float(row[0]) if row else 1.0


def process_symbol(conn, symbol: str):
    rows = conn.execute(LATEST_PER_SOURCE_SQL, {"symbol": symbol}).fetchall()
    if not rows:
        return

    prices = {row[0]: float(row[1]) for row in rows}
    currency = rows[0][2]

    outlier_flags = detect_outliers(prices)
    reliabilities = {}

    for source in prices:
        current = _get_reliability(conn, source)
        was_outlier = outlier_flags[source]
        updated = update_reliability(current, was_outlier)
        reliabilities[source] = updated

        conn.execute(UPSERT_RELIABILITY_SQL, {"source": source, "reliability": updated})

        if was_outlier:
            logger.warning("%s: source %s flagged as outlier (price=%s)", symbol, source, prices[source])

    final_price = consensus_price(prices, reliabilities)

    conn.execute(
        INSERT_CONSENSUS_SQL,
        {"symbol": symbol, "price": final_price, "currency": currency},
    )

    logger.info("%s: consensus=%.2f from %d source(s) %s", symbol, final_price, len(prices), list(prices))


def run():
    with engine.begin() as conn:
        symbols = [row[0] for row in conn.execute(DISTINCT_SYMBOLS_SQL).fetchall()]
        for symbol in symbols:
            process_symbol(conn, symbol)


if __name__ == "__main__":
    run()
