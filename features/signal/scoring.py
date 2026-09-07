import math


def rsi_score(rsi: float) -> float:
    """RSI is already 0-100 and reads directly as momentum strength — no transform needed."""
    return rsi


def macd_score(macd_histogram: float, reference_price: float) -> float:
    """Normalize the histogram against price scale (gold prices are huge numbers in IRR),
    then squash into 0-100 with a bullish/bearish midpoint at 50."""
    if not reference_price:
        return 50.0
    normalized = macd_histogram / reference_price
    return 50 + 50 * math.tanh(normalized * 500)


def technical_score(
    rsi: float | None,
    macd_histogram: float | None,
    reference_price: float | None,
) -> float | None:
    parts = []
    if rsi is not None:
        parts.append(rsi_score(rsi))
    if macd_histogram is not None and reference_price:
        parts.append(macd_score(macd_histogram, reference_price))

    if not parts:
        return None
    return sum(parts) / len(parts)


def premium_score(premium_pct: float, sensitivity: float = 5.0) -> float:
    """Cheaper than fair value (negative premium) leans bullish; pricier leans bearish."""
    score = 50 - premium_pct * sensitivity
    return max(0.0, min(100.0, score))
