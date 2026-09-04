-- Gold Intelligence Platform — Phase 0/1 Schema
-- اصل کلیدی: raw_prices هیچ‌وقت overwrite نمی‌شه؛ هر رکورد خام از هر منبع جدا ذخیره می‌شه.

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ============================================================
-- 1) RAW PRICES — قیمت خام از هر منبع، بدون هیچ پردازشی
-- ============================================================
CREATE TABLE IF NOT EXISTS raw_prices (
    id              BIGSERIAL,
    source          TEXT        NOT NULL,   -- مثلا 'tgju', 'alanchand', 'goldapi'
    symbol          TEXT        NOT NULL,   -- مثلا 'gold_18k', 'coin_emami', 'xau_usd', 'usd_irr'
    price           NUMERIC     NOT NULL,
    currency        TEXT        NOT NULL,   -- 'IRR' یا 'USD'
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    raw_payload     JSONB,                  -- پاسخ خام API/HTML برای دیباگ بعدی
    PRIMARY KEY (id, fetched_at)
);

-- تبدیل به hypertable برای بهره‌وری سری‌زمانی (TimescaleDB)
SELECT create_hypertable('raw_prices', 'fetched_at', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_raw_prices_source_symbol_time
    ON raw_prices (source, symbol, fetched_at DESC);

-- ============================================================
-- 2) CONSENSUS PRICES — قیمت نهایی بعد از ترکیب منابع (فاز ۶ پر می‌شه، فعلا خالیه)
-- ============================================================
CREATE TABLE IF NOT EXISTS consensus_prices (
    id              BIGSERIAL,
    symbol          TEXT        NOT NULL,
    price           NUMERIC     NOT NULL,
    currency        TEXT        NOT NULL,
    method          TEXT        NOT NULL DEFAULT 'simple_avg', -- بعدا 'reliability_weighted'
    computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, computed_at)
);

SELECT create_hypertable('consensus_prices', 'computed_at', if_not_exists => TRUE);

-- ============================================================
-- 3) PREMIUM / BUBBLE — فاز ۲ و ۷ این جدول رو پر می‌کنن
-- ============================================================
CREATE TABLE IF NOT EXISTS gold_premium (
    id                  BIGSERIAL,
    symbol              TEXT        NOT NULL,   -- 'gold_18k', 'coin_emami', ...
    theoretical_price   NUMERIC     NOT NULL,
    actual_price        NUMERIC     NOT NULL,
    premium_pct         NUMERIC     NOT NULL,
    premium_zscore      NUMERIC,                -- فاز ۷ پر می‌شه
    computed_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, computed_at)
);

SELECT create_hypertable('gold_premium', 'computed_at', if_not_exists => TRUE);

-- ============================================================
-- 4) SIGNALS — خروجی Signal Engine (فاز ۴ به بعد)
-- ============================================================
CREATE TABLE IF NOT EXISTS signals (
    id              BIGSERIAL,
    symbol          TEXT        NOT NULL,
    horizon         TEXT        NOT NULL,   -- '1D', '7D', '30D', '90D'
    signal          TEXT        NOT NULL,   -- 'BUY', 'HOLD', 'SELL'
    score           NUMERIC     NOT NULL,   -- 0-100
    confidence      TEXT,                   -- 'LOW', 'MEDIUM', 'HIGH'
    reasoning       JSONB,                  -- breakdown امتیازها، فاز ۹ توسط LLM انسانی می‌شه
    generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, generated_at)
);

SELECT create_hypertable('signals', 'generated_at', if_not_exists => TRUE);

-- ============================================================
-- 5) SOURCE RELIABILITY — فاز ۶
-- ============================================================
CREATE TABLE IF NOT EXISTS source_reliability (
    source          TEXT        PRIMARY KEY,
    reliability     NUMERIC     NOT NULL DEFAULT 1.0,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
