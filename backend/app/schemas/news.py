from datetime import datetime
from typing import Any

from pydantic import BaseModel


class NewsItemOut(BaseModel):
    source: str
    title: str
    url: str
    summary: str | None
    published_at: datetime | None
    event: str | None
    assets: list[Any] | None
    direction: str | None
    importance: float | None
    classified_at: datetime | None

    class Config:
        from_attributes = True
