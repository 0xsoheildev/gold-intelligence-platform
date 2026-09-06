import pandas as pd


def sma(prices: pd.Series, window: int = 20) -> float | None:
    if len(prices) < window:
        return None
    return float(prices.rolling(window).mean().iloc[-1])


def ema(prices: pd.Series, span: int = 20) -> float | None:
    if len(prices) < span:
        return None
    return float(prices.ewm(span=span, adjust=False).mean().iloc[-1])


def rsi(prices: pd.Series, window: int = 14) -> float | None:
    if len(prices) < window + 1:
        return None

    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    last_avg_loss = avg_loss.iloc[-1]
    if last_avg_loss == 0:
        return 100.0

    rs = avg_gain.iloc[-1] / last_avg_loss
    return float(100 - (100 / (1 + rs)))


def macd(
    prices: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple[float | None, float | None, float | None]:
    if len(prices) < slow + signal:
        return None, None, None

    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return (
        float(macd_line.iloc[-1]),
        float(signal_line.iloc[-1]),
        float(histogram.iloc[-1]),
    )
