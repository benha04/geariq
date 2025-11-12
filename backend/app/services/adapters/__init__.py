from typing import List, Dict, Any
from .impact import search as impact_search

async def fetch_candidates(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Call available adapters and return concatenated normalized results.

    Currently only Impact adapter is registered. Each adapter should return a
    list of product dicts with keys: title, url, retailer, price, rating, shipping_days.
    """
    results: List[Dict[str, Any]] = []

    # Impact
    try:
        impact = await impact_search(query, budget)
        if impact:
            results.extend(impact)
    except Exception:
        # Log in real code; silent fallback for now
        pass

    return results
