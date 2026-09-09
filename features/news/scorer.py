DIRECTION_MULTIPLIER = {
    "bullish_gold": 1,
    "bearish_gold": -1,
    "neutral": 0,
}


def news_score(classified_items: list[dict]) -> float | None:
    """Each item is {"direction": ..., "importance": ...}. Weighted by importance so a
    single high-impact headline outweighs several low-importance ones."""
    weighted_sum = 0.0
    total_weight = 0.0

    for item in classified_items:
        importance = item.get("importance") or 0.0
        direction = item.get("direction", "neutral")
        multiplier = DIRECTION_MULTIPLIER.get(direction, 0)

        value = 50 + 50 * multiplier * importance
        weight = max(importance, 0.05)  # even "unimportant" items count a little, not zero

        weighted_sum += value * weight
        total_weight += weight

    if total_weight == 0:
        return None
    return weighted_sum / total_weight
