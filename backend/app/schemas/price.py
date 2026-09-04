from datetime import datetime
from pydantic import BaseModel


class PriceOut(BaseModel):
    source: str
    symbol: str
    price: float
    currency: str
    fetched_at: datetime

    class Config:
        from_attributes = True
