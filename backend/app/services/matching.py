from typing import List, Dict, Any

# v0: simple weighted score; later: embeddings + rules
WEIGHTS = {"price": 0.5, "rating": 0.3, "shipping": 0.2}

def score(candidate: Dict[str, Any]) -> float:
    price = candidate.get("price", 1e9)
    rating = candidate.get("rating", 0)
    shipping_days = candidate.get("shipping_days", 7)
    price_norm = 1.0 / max(price, 1.0)
    rating_norm = rating / 5.0
    shipping_norm = 1.0 / max(shipping_days, 1)
    return (WEIGHTS["price"]*price_norm + WEIGHTS["rating"]*rating_norm + WEIGHTS["shipping"]*shipping_norm)

def pick_best(candidates: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    if not candidates:
        return None
    return max(candidates, key=score)
