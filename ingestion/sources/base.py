from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class PricePoint:
    """یک قیمت خام از یک منبع، آماده برای insert در raw_prices."""
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
    """
    قرارداد مشترک همه‌ی منابع.
    هر منبع جدید (چه ایرانی چه جهانی) فقط باید fetch() رو پیاده‌سازی کنه
    و لیستی از PricePoint برگردونه — بقیه‌ی pipeline (ذخیره‌سازی، validation) مشترکه.
    """

    name: str

    @abstractmethod
    def fetch(self) -> list[PricePoint]:
        ...
