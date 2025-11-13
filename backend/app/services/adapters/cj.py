import asyncio
from typing import List, Dict, Any
import os
from app.services.catalog import search_catalog


async def _call_cj_api(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # Placeholder for a real CJ API call. If an API key is set, implement the
    # real integration here and return normalized items.
    await asyncio.sleep(0)
    return []


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # If CJ API key present, attempt live call; otherwise return catalog fallback
    key = os.getenv("CJ_API_KEY")
    if key:
        items = await _call_cj_api(query, budget)
        if items:
            return items

    # development fallback
    return search_catalog(query, top_n=10)


async def search_parsed(parsed_query) -> List[Dict[str, Any]]:
    # Respect parsed constraints if provided
    q = getattr(parsed_query, "q", "")
    budget = getattr(getattr(parsed_query, "constraints", None), "budget", None)
    return await search(q, budget)
