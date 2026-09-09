"""
Generates synthetic historical price points so Phase 3 indicators (which need
30-40+ data points to produce non-null RSI/MACD values) can be tested without
waiting days for the real scheduler to accumulate data.

Points are tagged with source='seed_synthetic' so they're easy to tell apart
from real data and to delete afterwards.

Usage:
    python -m scripts.seed_data
    python -m scripts.seed_data --symbol gold_18k --points 60 --interval-minutes 10

Cleanup once you're done testing:
    DELETE FROM raw_prices WHERE source = 'seed_synthetic';
"""

import argparse
import random
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

from ingestion.db import save_price_points
from ingestion.sources.base import PricePoint

BASE_PRICES = {
    "gold_18k": 236_744_000,
    "coin_emami": 2_374_950_000,
    "coin_half": 1_210_000_000,
    "coin_quarter": 655_000_000,
    "coin_gerami": 350_000_000,
    "usd_irr": 2_272_050,
    "xau_usd": 4430.18,
}


def generate_walk(base_price: float, points: int, step_pct_std: float = 0.004) -> list[float]:
    """Random walk starting from base_price, each step moving by a small random percentage."""
    prices = [base_price]
    for _ in range(points - 1):
        change = random.gauss(0, step_pct_std)
        prices.append(prices[-1] * (1 + change))
    return prices


def seed(symbol: str, points: int, interval_minutes: int):
    if symbol not in BASE_PRICES:
        raise ValueError(f"unknown symbol '{symbol}', pick one of {list(BASE_PRICES)}")

    currency = "USD" if symbol == "xau_usd" else "IRR"
    prices = generate_walk(BASE_PRICES[symbol], points)

    now = datetime.now(timezone.utc)
    price_points = [
        PricePoint(
            source="seed_synthetic",
            symbol=symbol,
            price=price,
            currency=currency,
            fetched_at=now - timedelta(minutes=interval_minutes * (points - 1 - i)),
            raw_payload={"note": "synthetic data for local testing"},
        )
        for i, price in enumerate(prices)
    ]

    saved = save_price_points(price_points)
    print(f"seeded {saved} synthetic points for {symbol}, spanning {interval_minutes * (points - 1)} minutes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="gold_18k")
    parser.add_argument("--points", type=int, default=60)
    parser.add_argument("--interval-minutes", type=int, default=10)
    args = parser.parse_args()

    seed(args.symbol, args.points, args.interval_minutes)
