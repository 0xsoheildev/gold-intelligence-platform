<div align="center">

# 🥇 Gold Intelligence Platform

**Iranian gold market intelligence — data ingestion, technical analysis, and LLM-explained trading signals**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-TimescaleDB-336791?logo=postgresql&logoColor=white)](https://www.timescale.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-orange)]()

</div>

---

## What is this?

A system that collects gold and coin prices from Iranian and global markets, cross-references them against USD/IRR exchange rates, tracks the local market "premium" (bubble), ingests financial news, and produces a **buy / hold / sell signal — with a confidence score and a plain-language explanation, not just a label.**

Unlike a naive "feed prices and news into an LLM" approach, the decision-making here is **deterministic**: technical indicators, premium valuation, and news impact are scored numerically first. The LLM's job is to *explain* the result — not to calculate it.

```
Signal (7D):  BUY      Confidence: HIGH  (Score: 78)
Signal (30D): BUY      Confidence: MEDIUM (Score: 65)
Signal (90D): HOLD     Confidence: LOW    (Score: 52)

Reasons:
+ Gold momentum is positive (Technical Score: 79)
+ USD/IRR trend is upward
+ Current premium is below its 90-day average (Z-score: -0.8)
+ Recent news sentiment is moderately bullish

Risk: Medium — elevated short-term volatility
Invalidation: USD/IRR drops below X, or gold breaks below Y
```

---

## ✨ Key ideas

- 📥 **Multi-source ingestion** — Iranian gold/coin markets + global XAU/USD, never overwriting raw data
- 🧮 **Deterministic signal engine** — technical indicators, premium/bubble valuation with historical Z-scores, and news impact scoring, combined with transparent weights
- 🗞️ **Structured news intelligence** — deduplication and event classification instead of naive sentiment
- 🧠 **LLM as analyst, not oracle** — the model explains a decision that was already made numerically
- 🔁 **Backtested, not guessed** — signal thresholds are calibrated against historical data
- 📱 **Multi-surface** — REST API → Telegram bot → web dashboard → native Android app (Kotlin/Compose)

---

## 🏗️ Architecture

```
                    DATA SOURCES
        ┌────────────────┼────────────────┐
   Iranian markets   Global markets      News
   (scraping)         (XAU/USD API)   (RSS/News API)
        └────────────────┼────────────────┘
                         ↓
                 INGESTION LAYER
                         ↓
              RAW STORAGE (append-only)
                         ↓
              DATA QUALITY LAYER
        (outlier detection · source reliability)
                         ↓
              FEATURE ENGINEERING
        ┌────────────────┼────────────────┐
   Technical           Premium /          News /
   (RSI, MACD, …)      Bubble (Z-score)   Event Intelligence
        └────────────────┼────────────────┘
                         ↓
                  SIGNAL ENGINE
                         ↓
                  BACKTEST ENGINE
                         ↓
                LLM EXPLANATION LAYER
                         ↓
                   FastAPI  →  Telegram bot · Web dashboard · Android app
```

---

## 🧰 Tech stack

| Layer | Choice |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL + TimescaleDB |
| Data processing | Pandas / Polars |
| Scheduling | APScheduler → Celery/Kafka (later phases) |
| Scraping | httpx, BeautifulSoup, Playwright |
| ML (later phase) | scikit-learn, XGBoost |
| LLM | Claude API — explanation only, never decision-making |
| Web dashboard | Next.js |
| Mobile app | Kotlin, Jetpack Compose |
| Infra | Docker Compose |

---

## 🚀 Getting started

```bash
git clone https://github.com/0xsoheildev/gold-intelligence.git
cd gold-intelligence
cp .env.example .env
# add your GOLDAPI_KEY (free tier at goldapi.io) to .env

docker compose up -d db       # start the database
docker compose up -d --build backend   # start the API on http://localhost:8000
```

API docs: `http://localhost:8000/docs`

Run the ingestion scheduler (fetches Iranian + global prices every 10 minutes):

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence
export GOLDAPI_KEY=your_key_here
python -m ingestion.scheduler
```

Compute the current gold premium (theoretical vs. actual price):

```bash
python -m features.premium.runner
curl http://localhost:8000/premium/current
```

Compute technical indicators (SMA, EMA, RSI, MACD) once you have enough price history (30-40+ points):

```bash
python -m features.technical.runner
curl http://localhost:8000/technical/current
```

> Need to test before real data accumulates? Seed synthetic price history with `python -m scripts.seed_data --symbol gold_18k --points 60`, then clean it up afterward with `DELETE FROM raw_prices WHERE source = 'seed_synthetic';`.

> **macOS note**: if `pip install` fails building `psycopg` or `pydantic-core` from source, your local Python is likely too new (e.g. 3.14) for some packages' prebuilt wheels. Use Python 3.12 for the virtualenv instead: `brew install python@3.12 && python3.12 -m venv venv`.

---

## 🗺️ Roadmap

- [x] **Phase 0** — Product design
- [x] **Phase 1** — Data ingestion + raw storage *(verified end-to-end)*
- [x] **Phase 2** — Premium / bubble engine *(verified end-to-end)*
- [x] **Phase 3** — Technical indicators engine *(verified end-to-end)*
- [ ] **Phase 4** — Signal engine (v1)
- [ ] **Phase 5** — News / event intelligence
- [ ] **Phase 6** — Data quality layer (outlier detection, source reliability)
- [ ] **Phase 7** — Premium Z-score + multi-horizon signals
- [ ] **Phase 8** — Backtesting engine
- [ ] **Phase 9** — LLM explanation layer
- [ ] **Phase 9.5** — Kafka event streaming (optional)
- [ ] **Phase 10** — Web dashboard
- [ ] **Phase 11** — Android app
- [ ] **Phase 12** — Hardening & production

---

## ⚠️ Disclaimer

This project is for educational and research purposes. Signals produced by this system are **not financial advice**. Always do your own research before making investment decisions.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.