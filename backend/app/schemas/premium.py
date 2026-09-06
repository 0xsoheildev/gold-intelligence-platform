from datetime import datetime
from pydantic import BaseModel


class PremiumOut(BaseModel):
    symbol: str
    theoretical_price: float
    actual_price: float
    premium_pct: float
    premium_zscore: float | None
    computed_at: datetime

    class Config:
        from_attributes = True
