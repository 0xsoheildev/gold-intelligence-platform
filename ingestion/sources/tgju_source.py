"""
Iranian Source: TGJU.org
"""

import re

import httpx
from bs4 import BeautifulSoup

from ingestion.sources.base import BaseSource, PricePoint

BASE_URL = "https://www.tgju.org/profile/"

SYMBOL_SLUGS = {
    "gold_18k": "geram18",
    "coin_emami": "sekee",
    "coin_half": "nim",
    "coin_quarter": "rob",
    "coin_gerami": "gerami",
    "usd_irr": "price_dollar_rl",
}


def _extract_price(soup: BeautifulSoup) -> float | None:
    text = soup.get_text(" ", strip=True)
    match = re.search(r"قیمت لحظه‌ای\D{0,30}([\d,]{5,})", text)
    if match:
        return float(match.group(1).replace(",", ""))

    match = re.search(r"([\d,]{6,})", text)
    if match:
        return float(match.group(1).replace(",", ""))

    return None


class TgjuSource(BaseSource):
    name = "tgju"

    def fetch(self) -> list[PricePoint]:
        points: list[PricePoint] = []

        for symbol, slug in SYMBOL_SLUGS.items():
            url = f"{BASE_URL}{slug}"
            try:
                response = httpx.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
            except httpx.HTTPError:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            price = _extract_price(soup)
            if price is None:
                continue

            points.append(
                PricePoint(
                    source=self.name,
                    symbol=symbol,
                    price=price,
                    currency="IRR",
                    raw_payload={"url": url},
                )
            )

        return points


if __name__ == "__main__":
    source = TgjuSource()
    for p in source.fetch():
        print(p)
