import httpx
from bs4 import BeautifulSoup


def fetch_article_text(url: str, max_chars: int = 3000) -> str:
    """Best-effort scrape of an article's paragraph text. Returns an empty
    string on any failure — classification still works from the title alone
    in that case, it's just less informed."""
    try:
        response = httpx.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except httpx.HTTPError:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = " ".join(p for p in paragraphs if p)
    return text[:max_chars]
