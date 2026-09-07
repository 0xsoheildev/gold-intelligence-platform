"""
Target weights match the full design (technical/premium/macro/news/regime).
Only technical + premium are wired up in Phase 4 — the rest default to
unavailable and get renormalized out until Phase 5+ fills them in.
"""

TARGET_WEIGHTS = {
    "technical": 25,
    "premium": 20,
    # "macro_fx": 20,      -- Phase 5+
    # "news": 15,          -- Phase 5
    # "regime": 10,        -- later phase
}

BUY_THRESHOLD = 60
SELL_THRESHOLD = 40


def combine(components: dict[str, float | None]) -> dict:
    available = {k: v for k, v in components.items() if v is not None}

    if not available:
        return {"score": None, "signal": None, "confidence": None, "components": {}}

    total_weight = sum(TARGET_WEIGHTS[k] for k in available)
    final_score = sum(available[k] * TARGET_WEIGHTS[k] for k in available) / total_weight

    if final_score >= BUY_THRESHOLD:
        signal = "BUY"
    elif final_score <= SELL_THRESHOLD:
        signal = "SELL"
    else:
        signal = "HOLD"

    # Thresholds and the confidence rule below are a starting point — Phase 8
    # backtesting is what actually calibrates these, not guesswork.
    distance_from_neutral = abs(final_score - 50)
    all_components_available = len(available) == len(TARGET_WEIGHTS)

    if not all_components_available:
        confidence = "LOW"
    elif distance_from_neutral >= 20:
        confidence = "HIGH"
    elif distance_from_neutral >= 10:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return {
        "score": final_score,
        "signal": signal,
        "confidence": confidence,
        "components": available,
    }
