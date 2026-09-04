from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP, JSON, func

from app.core.db import Base


class RawPrice(Base):
    """
    قیمت خام از یک منبع مشخص، در یک لحظه‌ی مشخص.
    اصل کلیدی: هیچ‌وقت این جدول overwrite/update نمی‌شه — فقط insert.
    """
    __tablename__ = "raw_prices"

    id = Column(BigInteger, primary_key=True)
    source = Column(String, nullable=False)        # 'tgju', 'goldapi', ...
    symbol = Column(String, nullable=False)         # 'gold_18k', 'xau_usd', 'usd_irr', ...
    price = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)        # 'IRR' یا 'USD'
    fetched_at = Column(TIMESTAMP(timezone=True), primary_key=True, server_default=func.now())
    raw_payload = Column(JSON, nullable=True)
