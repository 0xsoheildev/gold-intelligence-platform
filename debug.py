from dotenv import load_dotenv
load_dotenv()
import os
from google import genai
from google.genai.types import GenerateContentConfig

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

prompt = """Classify this financial news article for a gold market signal system.
Read the full article at the URL below before classifying.
Respond with ONLY a JSON object, no other text, with these fields:
- event: short UPPER_SNAKE_CASE label
- assets: array from ["gold", "usd", "oil", "equities"]
- direction: one of "bullish_gold", "bearish_gold", "neutral"
- importance: number from 0 to 1

Title: Gold edges down as strong payrolls revive Fed hike bets
URL: https://www.investing.com/news/commodities-news/gold-holds-near-4400-as-strong-payrolls-iran-tensions-lift-fed-hike-bets-4890334"""

resp = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=GenerateContentConfig(tools=[{"url_context": {}}]),
)
print("RAW RESPONSE TEXT:")
print(repr(resp.text))