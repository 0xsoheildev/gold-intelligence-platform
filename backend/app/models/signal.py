from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP, JSON, func

from app.core.db import Base


class Signal(Base):
    __tablename__ = "signals"

    id = Column(BigInteger, primary_key=True)
    symbol = Column(String, nullable=False)
    horizon = Column(String, nullable=False)
    signal = Column(String, nullable=False)
    score = Column(Numeric, nullable=False)
    confidence = Column(String, nullable=True)
    reasoning = Column(JSON, nullable=True)
    generated_at = Column(TIMESTAMP(timezone=True), primary_key=True, server_default=func.now())
