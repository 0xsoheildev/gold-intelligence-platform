DECAY = 0.9  # how much past history counts vs. this round's result


def update_reliability(current: float, was_outlier: bool) -> float:
    """Exponential moving average: being an outlier drags the score toward 0,
    being consistent with the group nudges it back toward 1. A source that's
    wrong once doesn't get blacklisted — it takes a pattern to move the score
    meaningfully."""
    target = 0.0 if was_outlier else 1.0
    return current * DECAY + target * (1 - DECAY)
