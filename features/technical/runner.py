import logging
import os

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
from sqlalchemy import create_engine, text

from features.technical.indicators import ema, macd, rsi, sma

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("technical_runner")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

PRICE_HISTORY_SQL = text(
    """
    SELECT price, fetched_at FROM raw_prices
    WHERE symbol = :symbol
    ORDER BY fetched_at ASC
    """
)

INSERT_TECHNICAL_SQL = text(
    """
    INSERT INTO technical_indicators (symbol, sma, ema, rsi, macd, macd_signal, macd_histogram)
    VALUES (:symbol, :sma, :ema, :rsi, :macd, :macd_signal, :macd_histogram)
    """
)


def _load_price_series(conn, symbol: str) -> pd.Series:
    rows = conn.execute(PRICE_HISTORY_SQL, {"symbol": symbol}).fetchall()
    prices = [float(row[0]) for row in rows]
    return pd.Series(prices)


def run(symbol: str = "gold_18k"):
    with engine.begin() as conn:
        prices = _load_price_series(conn, symbol)

        if len(prices) < 2:
            logger.warning("not enough data points for %s yet (%d), skipping", symbol, len(prices))
            return

        macd_line, macd_signal, macd_hist = macd(prices)

        result = {
            "symbol": symbol,
            "sma": sma(prices),
            "ema": ema(prices),
            "rsi": rsi(prices),
            "macd": macd_line,
            "macd_signal": macd_signal,
            "macd_histogram": macd_hist,
        }

        conn.execute(INSERT_TECHNICAL_SQL, result)

    logger.info("%s: %s", symbol, {k: v for k, v in result.items() if k != "symbol"})


if __name__ == "__main__":
    run()
