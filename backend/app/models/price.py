from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP, JSON, func

from app.core.db import Base


class RawPrice(Base):
    __tablename__ = "raw_prices"

    id = Column(BigInteger, primary_key=True)
    source = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    fetched_at = Column(TIMESTAMP(timezone=True), primary_key=True, server_default=func.now())
    raw_payload = Column(JSON, nullable=True)
