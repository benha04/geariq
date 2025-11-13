import asyncio
from typing import List, Dict, Any
import os
from app.services.catalog import search_catalog


async def _call_rakuten_api(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # Placeholder for a real Rakuten API call. Implement if credentials are present.
    await asyncio.sleep(0)
    return []


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    key = os.getenv("RAKUTEN_API_KEY")
    if key:
        items = await _call_rakuten_api(query, budget)
        if items:
            return items

    return search_catalog(query, top_n=10)


async def search_parsed(parsed_query) -> List[Dict[str, Any]]:
    q = getattr(parsed_query, "q", "")
    budget = getattr(getattr(parsed_query, "constraints", None), "budget", None)
    return await search(q, budget)
