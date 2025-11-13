from typing import List, Dict, Any, Tuple

# Configurable weights for v0 ranking
WEIGHTS = {"price": 0.5, "rating": 0.3, "shipping": 0.2}


def score_breakdown(candidate: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
    """Return total score and per-dimension contributions.

    Normalization:
    - price_norm = 1 / price (lower better)
    - rating_norm = rating / 5
    - shipping_norm = 1 / shipping_days
    """
    price = candidate.get("price", 1e9) or 1e9
    rating = candidate.get("rating", 0) or 0
    shipping_days = candidate.get("shipping_days", 7) or 7

    price_norm = 1.0 / max(price, 1.0)
    rating_norm = max(0.0, min(1.0, rating / 5.0))
    shipping_norm = 1.0 / max(shipping_days, 1)

    c_price = WEIGHTS["price"] * price_norm
    c_rating = WEIGHTS["rating"] * rating_norm
    c_shipping = WEIGHTS["shipping"] * shipping_norm

    total = c_price + c_rating + c_shipping
    breakdown = {"price": c_price, "rating": c_rating, "shipping": c_shipping, "total": total}
    return total, breakdown


def pick_best(candidates: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    if not candidates:
        return None
    best = None
    best_score = -1.0
    for c in candidates:
        sc, bd = score_breakdown(c)
        # attach breakdown so API can explain
        c["score_breakdown"] = bd
        if sc > best_score:
            best_score = sc
            best = c
    return best
