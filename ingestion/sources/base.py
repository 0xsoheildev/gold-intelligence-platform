from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class PricePoint:
    source: str
    symbol: str
    price: float
    currency: str
    raw_payload: dict | None = None
    fetched_at: datetime = None

    def __post_init__(self):
        if self.fetched_at is None:
            self.fetched_at = datetime.now(timezone.utc)


class BaseSource(ABC):
    name: str

    @abstractmethod
    def fetch(self) -> list[PricePoint]:
        ...
