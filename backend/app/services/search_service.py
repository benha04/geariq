from typing import List, Dict, Any
from app.services.adapters import fetch_candidates


async def search_marketplaces(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Fetch product candidates from registered adapters and return normalized results.

    Adapters should normalize to a common format. If no adapters return results,
    this function will return an empty list.
    """
    candidates = await fetch_candidates(query, budget)
    # adapters are expected to return normalized dicts; ensure budget filtering as a safeguard
    if budget is not None:
        filtered: List[Dict[str, Any]] = []
        for d in candidates:
            price_val = d.get("price", 0.0)
            if isinstance(price_val, (int, float)):
                price_f = float(price_val)
            elif isinstance(price_val, str):
                try:
                    price_f = float(price_val)
                except ValueError:
                    price_f = 0.0
            else:
                price_f = 0.0

            if price_f <= budget:
                filtered.append(d)

        candidates = filtered

    return candidates
