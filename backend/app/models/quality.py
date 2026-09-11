from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP, func

from app.core.db import Base


class ConsensusPrice(Base):
    __tablename__ = "consensus_prices"

    id = Column(BigInteger, primary_key=True)
    symbol = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    method = Column(String, nullable=False)
    computed_at = Column(TIMESTAMP(timezone=True), primary_key=True, server_default=func.now())


class SourceReliability(Base):
    __tablename__ = "source_reliability"

    source = Column(String, primary_key=True)
    reliability = Column(Numeric, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
