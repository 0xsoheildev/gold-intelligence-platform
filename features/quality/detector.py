def detect_outliers(prices: dict[str, float], threshold_pct: float = 12.0) -> dict[str, bool]:
    """Given {source: price} for the same symbol at roughly the same time,
    flag any source whose price deviates more than threshold_pct from the
    median of all sources.

    Needs at least 3 sources to be meaningful: with exactly 2, the median is
    just their midpoint, so both sources end up equidistant from it and a
    single bad source would get its "wrong" price averaged in as if it were
    a legitimate vote — flagging both as outliers blames the correct source
    just as often as the broken one. Wait for a third source to break the tie."""
    if len(prices) < 3:
        return {source: False for source in prices}

    values = sorted(prices.values())
    n = len(values)
    median = values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2

    return {
        source: abs(price - median) / median * 100 > threshold_pct
        for source, price in prices.items()
    }
