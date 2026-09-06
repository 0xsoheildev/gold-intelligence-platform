import logging
import os

from sqlalchemy import create_engine, text

from features.premium.calculator import premium_pct, theoretical_gold_18k_price

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("premium_runner")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

LATEST_PRICE_SQL = text(
    """
    SELECT price FROM raw_prices
    WHERE symbol = :symbol
    ORDER BY fetched_at DESC
    LIMIT 1
    """
)

INSERT_PREMIUM_SQL = text(
    """
    INSERT INTO gold_premium (symbol, theoretical_price, actual_price, premium_pct)
    VALUES (:symbol, :theoretical_price, :actual_price, :premium_pct)
    """
)


def _latest_price(conn, symbol: str) -> float | None:
    row = conn.execute(LATEST_PRICE_SQL, {"symbol": symbol}).fetchone()
    return float(row[0]) if row else None


def run():
    with engine.begin() as conn:
        xau_usd = _latest_price(conn, "xau_usd")
        usd_irr = _latest_price(conn, "usd_irr")
        gold_18k = _latest_price(conn, "gold_18k")

        if xau_usd is None or usd_irr is None or gold_18k is None:
            logger.warning("missing one of xau_usd / usd_irr / gold_18k, skipping this cycle")
            return

        theoretical = theoretical_gold_18k_price(xau_usd, usd_irr)
        premium = premium_pct(gold_18k, theoretical)

        conn.execute(
            INSERT_PREMIUM_SQL,
            {
                "symbol": "gold_18k",
                "theoretical_price": theoretical,
                "actual_price": gold_18k,
                "premium_pct": premium,
            },
        )

    logger.info(
        "gold_18k: theoretical=%.0f actual=%.0f premium=%.2f%%",
        theoretical,
        gold_18k,
        premium,
    )


if __name__ == "__main__":
    run()
