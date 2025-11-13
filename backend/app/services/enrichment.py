from typing import List, Dict, Any
import asyncio


async def enrich_offers_shortlist(candidates: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """Pretend to call retailer APIs for the top_k candidates to refresh price/stock.

    Currently this is a no-op that simulates a small async wait and returns candidates as-is.
    """
    await asyncio.sleep(0)
    # In real flow: call each candidate.url and refresh price/in_stock/shipping_days
    return candidates[:top_k]
