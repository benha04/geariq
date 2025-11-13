import os
from typing import List, Dict, Any
import httpx

from app.services.catalog import search_catalog


async def _call_scrapeless(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Call Scrapeless (a Google Search scraping API) to retrieve product links.

    Expect environment variables:
    - SCRAPELESS_API_KEY (required when using Scrapeless)
    - SCRAPELESS_BASE (optional)

    Scrapeless returns a JSON payload that may include an array of results.
    We normalize a subset of fields into the adapter shape used by the search
    pipeline. On any error or missing key, return an empty list.
    """
    key = os.getenv("SCRAPELESS_API_KEY")
    if not key:
        return []

    base = os.getenv("SCRAPELESS_BASE") or "https://api.scrapeless.com"
    url = f"{base}/search"
    params = {"q": query, "key": key}
    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("results") or data.get("items") or []
            mapped: List[Dict[str, Any]] = []
            for it in items:
                mapped.append({
                    "title": it.get("title") or it.get("name"),
                    "retailer": it.get("source") or it.get("domain"),
                    "price": it.get("price"),
                    "rating": None,
                    "shipping_days": None,
                    "url": it.get("link") or it.get("url"),
                    "matched_attributes": [],
                })
            return mapped
    except Exception:
        return []


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # Return results only when Scrapeless is configured and returns items.
    # Let the central search service handle the sample catalog fallback.
    results = await _call_scrapeless(query, budget)
    return results or []


async def search_parsed(parsed_query) -> List[Dict[str, Any]]:
    q = getattr(parsed_query, "q", "")
    budget = getattr(getattr(parsed_query, "constraints", None), "budget", None)
    return await search(q, budget)
