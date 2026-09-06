-- Gold Intelligence Platform — Phase 0/1 Schema
-- اصل کلیدی: raw_prices هیچ‌وقت overwrite نمی‌شه؛ هر رکورد خام از هر منبع جدا ذخیره می‌شه.

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS raw_prices (
    id              BIGSERIAL,
    source          TEXT        NOT NULL,
    symbol          TEXT        NOT NULL,
    price           NUMERIC     NOT NULL,
    currency        TEXT        NOT NULL,
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    raw_payload     JSONB,
    PRIMARY KEY (id, fetched_at)
);

SELECT create_hypertable('raw_prices', 'fetched_at', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_raw_prices_source_symbol_time
    ON raw_prices (source, symbol, fetched_at DESC);

CREATE TABLE IF NOT EXISTS consensus_prices (
    id              BIGSERIAL,
    symbol          TEXT        NOT NULL,
    price           NUMERIC     NOT NULL,
    currency        TEXT        NOT NULL,
    method          TEXT        NOT NULL DEFAULT 'simple_avg',
    computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, computed_at)
);

SELECT create_hypertable('consensus_prices', 'computed_at', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS gold_premium (
    id                  BIGSERIAL,
    symbol              TEXT        NOT NULL,
    theoretical_price   NUMERIC     NOT NULL,
    actual_price        NUMERIC     NOT NULL,
    premium_pct         NUMERIC     NOT NULL,
    premium_zscore      NUMERIC,
    computed_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, computed_at)
);

SELECT create_hypertable('gold_premium', 'computed_at', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS signals (
    id              BIGSERIAL,
    symbol          TEXT        NOT NULL,
    horizon         TEXT        NOT NULL,
    signal          TEXT        NOT NULL,
    score           NUMERIC     NOT NULL,
    confidence      TEXT,
    reasoning       JSONB,
    generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, generated_at)
);

SELECT create_hypertable('signals', 'generated_at', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS source_reliability (
    source          TEXT        PRIMARY KEY,
    reliability     NUMERIC     NOT NULL DEFAULT 1.0,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
