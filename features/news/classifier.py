import json
import logging
import os

from google import genai

logger = logging.getLogger("news_classifier")

# Free tier model — see https://ai.google.dev for current model names, they
# rotate faster than a typical package version.
CLASSIFIER_MODEL = "gemini-3.6-flash"

CLASSIFICATION_PROMPT = """Classify this financial news item for a gold market signal system.
Respond with ONLY a JSON object, no other text, with these fields:
- event: short UPPER_SNAKE_CASE label (e.g. FED_RATE_DECISION, GEOPOLITICAL_TENSION, CENTRAL_BANK_BUYING, INFLATION_DATA, USD_STRENGTH, OTHER)
- assets: array from ["gold", "usd", "oil", "equities"]
- direction: one of "bullish_gold", "bearish_gold", "neutral"
- importance: number from 0 to 1, how market-moving this is

Title: {title}
Article text: {article_text}"""


def _client() -> genai.Client | None:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def _strip_code_fence(text: str) -> str:
    """Gemini sometimes wraps JSON in ```json fences even when told not to."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.removesuffix("```").strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return text


def classify(title: str, article_text: str) -> dict | None:
    client = _client()
    if client is None:
        return None

    try:
        response = client.models.generate_content(
            model=CLASSIFIER_MODEL,
            contents=CLASSIFICATION_PROMPT.format(
                title=title,
                article_text=article_text or "(not available, classify from the title alone)",
            ),
        )
        raw_text = _strip_code_fence(response.text)
        return json.loads(raw_text)
    except Exception as e:
        # a single bad classification shouldn't take down the whole run,
        # but we do want to see *why* — rate limits, quota, bad JSON, etc.
        logger.warning("classification failed for %r: %s", title, e)
        return None
