def consensus_price(prices: dict[str, float], reliabilities: dict[str, float]) -> float:
    """Reliability-weighted average — an unreliable source pulls the result
    less than a trustworthy one, rather than being excluded outright, since
    a flaky source is still usually somewhat close to reality."""
    total_weight = sum(reliabilities.get(source, 1.0) for source in prices)
    if total_weight == 0:
        return sum(prices.values()) / len(prices)

    return sum(price * reliabilities.get(source, 1.0) for source, price in prices.items()) / total_weight
