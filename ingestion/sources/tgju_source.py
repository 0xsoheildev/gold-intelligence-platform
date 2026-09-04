"""
منبع ایرانی: tgju.org

نکته‌ی مهم: ساختار HTML سایت‌های ایرانی مدام تغییر می‌کنه. این پیاده‌سازی
یه نمونه‌ی کارکردیه که باید موقع اجرا selectors رو با inspect کردن صفحه‌ی
واقعی verify/به‌روزرسانی کنی. منطق pipeline (fetch → PricePoint → DB) ثابت
می‌مونه، فقط این فایل ممکنه نیاز به نگه‌داری دوره‌ای داشته باشه.
"""

import httpx
from bs4 import BeautifulSoup

from ingestion.sources.base import BaseSource, PricePoint

TGJU_URL = "https://www.tgju.org/"

# نگاشت id های جدول قیمت سایت به symbol داخلی خودمون
# این id ها رو باید با inspect کردن صفحه تایید/به‌روزرسانی کنی
SYMBOL_MAP = {
    "l-geram18": ("gold_18k", "IRR"),
    "l-sekee": ("coin_emami", "IRR"),
    "l-nim": ("coin_half", "IRR"),
    "l-rob": ("coin_quarter", "IRR"),
    "l-price_dollar_rl": ("usd_irr", "IRR"),
}


class TgjuSource(BaseSource):
    name = "tgju"

    def fetch(self) -> list[PricePoint]:
        response = httpx.get(TGJU_URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        points: list[PricePoint] = []
        for html_id, (symbol, currency) in SYMBOL_MAP.items():
            row = soup.find(id=html_id)
            if row is None:
                # منبع flaky ممکنه — این رو در فاز ۶ (Data Quality) به‌عنوان
                # missing-data لاگ می‌کنیم؛ فعلا فقط skip می‌کنیم
                continue

            price_text = row.find(class_="info-price")
            if price_text is None:
                continue

            raw_value = price_text.get_text(strip=True).replace(",", "")
            try:
                price = float(raw_value)
            except ValueError:
                continue

            points.append(
                PricePoint(
                    source=self.name,
                    symbol=symbol,
                    price=price,
                    currency=currency,
                    raw_payload={"raw_text": raw_value, "html_id": html_id},
                )
            )

        return points


if __name__ == "__main__":
    # تست دستی سریع
    source = TgjuSource()
    for p in source.fetch():
        print(p)
