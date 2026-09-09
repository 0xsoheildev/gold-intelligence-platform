"""
منبع جهانی: GoldAPI.io — نیاز به API key رایگان (ثبت‌نام در goldapi.io).
"""

import httpx

from ingestion.sources.base import BaseSource, PricePoint

GOLDAPI_URL = "https://www.goldapi.io/api/XAU/USD"


class GoldApiSource(BaseSource):
    name = "goldapi"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self) -> list[PricePoint]:
        headers = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json",
        }
        response = httpx.get(GOLDAPI_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        price = float(data["price"])

        return [
            PricePoint(
                source=self.name,
                symbol="xau_usd",
                price=price,
                currency="USD",
                raw_payload=data,
            )
        ]


if __name__ == "__main__":
    import os

    source = GoldApiSource(api_key=os.environ.get("GOLDAPI_KEY", ""))
    for p in source.fetch():
        print(p)
