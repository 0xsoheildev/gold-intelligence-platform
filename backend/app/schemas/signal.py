from datetime import datetime
from typing import Any

from pydantic import BaseModel


class SignalOut(BaseModel):
    symbol: str
    horizon: str
    signal: str
    score: float
    confidence: str | None
    reasoning: dict[str, Any] | None
    generated_at: datetime

    class Config:
        from_attributes = True
