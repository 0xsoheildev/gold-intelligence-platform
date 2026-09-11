from datetime import datetime
from pydantic import BaseModel


class ConsensusPriceOut(BaseModel):
    symbol: str
    price: float
    currency: str
    method: str
    computed_at: datetime

    class Config:
        from_attributes = True


class SourceReliabilityOut(BaseModel):
    source: str
    reliability: float
    updated_at: datetime

    class Config:
        from_attributes = True
