from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP, func

from app.core.db import Base


class GoldPremium(Base):
    __tablename__ = "gold_premium"

    id = Column(BigInteger, primary_key=True)
    symbol = Column(String, nullable=False)
    theoretical_price = Column(Numeric, nullable=False)
    actual_price = Column(Numeric, nullable=False)
    premium_pct = Column(Numeric, nullable=False)
    premium_zscore = Column(Numeric, nullable=True)  # filled in Phase 7
    computed_at = Column(TIMESTAMP(timezone=True), primary_key=True, server_default=func.now())
