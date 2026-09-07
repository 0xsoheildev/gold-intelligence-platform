import json
import logging
import os

from sqlalchemy import create_engine, text

from features.signal.engine import combine
from features.signal.scoring import premium_score, technical_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("signal_runner")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

LATEST_TECHNICAL_SQL = text(
    """
    SELECT rsi, macd_histogram FROM technical_indicators
    WHERE symbol = :symbol
    ORDER BY computed_at DESC
    LIMIT 1
    """
)

LATEST_PREMIUM_SQL = text(
    """
    SELECT premium_pct FROM gold_premium
    WHERE symbol = :symbol
    ORDER BY computed_at DESC
    LIMIT 1
    """
)

LATEST_PRICE_SQL = text(
    """
    SELECT price FROM raw_prices
    WHERE symbol = :symbol
    ORDER BY fetched_at DESC
    LIMIT 1
    """
)

INSERT_SIGNAL_SQL = text(
    """
    INSERT INTO signals (symbol, horizon, signal, score, confidence, reasoning)
    VALUES (:symbol, :horizon, :signal, :score, :confidence, CAST(:reasoning AS JSONB))
    """
)


def run(symbol: str = "gold_18k", horizon: str = "7D"):
    with engine.begin() as conn:
        technical_row = conn.execute(LATEST_TECHNICAL_SQL, {"symbol": symbol}).fetchone()
        premium_row = conn.execute(LATEST_PREMIUM_SQL, {"symbol": symbol}).fetchone()
        price_row = conn.execute(LATEST_PRICE_SQL, {"symbol": symbol}).fetchone()

        reference_price = float(price_row[0]) if price_row else None
        rsi = float(technical_row[0]) if technical_row and technical_row[0] is not None else None
        macd_hist = float(technical_row[1]) if technical_row and technical_row[1] is not None else None
        premium_pct = float(premium_row[0]) if premium_row else None

        tech_score = technical_score(rsi, macd_hist, reference_price)
        prem_score = premium_score(premium_pct) if premium_pct is not None else None

        result = combine({"technical": tech_score, "premium": prem_score})

        if result["score"] is None:
            logger.warning("no components available yet for %s, skipping", symbol)
            return

        conn.execute(
            INSERT_SIGNAL_SQL,
            {
                "symbol": symbol,
                "horizon": horizon,
                "signal": result["signal"],
                "score": result["score"],
                "confidence": result["confidence"],
                "reasoning": json.dumps(result["components"]),
            },
        )

    logger.info(
        "%s (%s): %s — score=%.1f confidence=%s components=%s",
        symbol,
        horizon,
        result["signal"],
        result["score"],
        result["confidence"],
        result["components"],
    )


if __name__ == "__main__":
    run()
