TROY_OUNCE_GRAMS = 31.1034768
GOLD_18K_PURITY = 0.75  # 18/24


def theoretical_gold_18k_price(xau_usd: float, usd_irr: float) -> float:
    """Theoretical IRR price per gram of 18k gold, derived from global spot price and FX rate."""
    price_per_gram_24k_irr = (xau_usd / TROY_OUNCE_GRAMS) * usd_irr
    return price_per_gram_24k_irr * GOLD_18K_PURITY


def premium_pct(actual_price: float, theoretical_price: float) -> float:
    """How far the local market price sits above (positive) or below (negative) fair value."""
    return (actual_price - theoretical_price) / theoretical_price * 100
