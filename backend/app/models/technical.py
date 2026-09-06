from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP, func

from app.core.db import Base


class TechnicalIndicators(Base):
    __tablename__ = "technical_indicators"

    id = Column(BigInteger, primary_key=True)
    symbol = Column(String, nullable=False)
    sma = Column(Numeric, nullable=True)
    ema = Column(Numeric, nullable=True)
    rsi = Column(Numeric, nullable=True)
    macd = Column(Numeric, nullable=True)
    macd_signal = Column(Numeric, nullable=True)
    macd_histogram = Column(Numeric, nullable=True)
    computed_at = Column(TIMESTAMP(timezone=True), primary_key=True, server_default=func.now())
