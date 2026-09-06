from datetime import datetime
from pydantic import BaseModel


class TechnicalOut(BaseModel):
    symbol: str
    sma: float | None
    ema: float | None
    rsi: float | None
    macd: float | None
    macd_signal: float | None
    macd_histogram: float | None
    computed_at: datetime

    class Config:
        from_attributes = True
