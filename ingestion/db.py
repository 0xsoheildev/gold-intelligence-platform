import json
import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

INSERT_SQL = text(
    """
    INSERT INTO raw_prices (source, symbol, price, currency, fetched_at, raw_payload)
    VALUES (:source, :symbol, :price, :currency, :fetched_at, CAST(:raw_payload AS JSONB))
    """
)


def save_price_points(points) -> int:
    if not points:
        return 0

    with engine.begin() as conn:
        for p in points:
            conn.execute(
                INSERT_SQL,
                {
                    "source": p.source,
                    "symbol": p.symbol,
                    "price": p.price,
                    "currency": p.currency,
                    "fetched_at": p.fetched_at,
                    "raw_payload": json.dumps(p.raw_payload) if p.raw_payload is not None else None,
                },
            )
    return len(points)
