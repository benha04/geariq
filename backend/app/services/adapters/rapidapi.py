import os
from typing import List, Dict, Any
import httpx

from app.services.catalog import search_catalog


async def _call_rapidapi(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Call a RapidAPI-hosted Real-Time Product Search endpoint.

    Expect environment variables:
    - RAPIDAPI_HOST (required when using RapidAPI)
    - RAPIDAPI_KEY (required when using RapidAPI)
    - RAPIDAPI_BASE (optional; if the provider uses a different base path)

    If the call fails or credentials are not present, return an empty list so
    the caller can fall back to the in-repo catalog.
    """
    host = os.getenv("RAPIDAPI_HOST")
    key = os.getenv("RAPIDAPI_KEY")
    if not host or not key:
        return []

    base = os.getenv("RAPIDAPI_BASE") or f"https://{host}"
    # Many RapidAPI endpoints use X-RapidAPI-Host and X-RapidAPI-Key headers
    url = f"{base}/search"
    params = {"q": query}
    if budget is not None:
        params["budget"] = budget

    headers = {
        "X-RapidAPI-Host": host,
        "X-RapidAPI-Key": key,
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            # normalize expected shapes: list or { items: [...] }
            items = data if isinstance(data, list) else data.get("items") or []
            mapped: List[Dict[str, Any]] = []
            for it in items:
                mapped.append({
                    "title": it.get("title") or it.get("name"),
                    "retailer": it.get("merchant") or it.get("retailer") or it.get("source"),
                    "price": it.get("price") or it.get("amount"),
                    "rating": it.get("rating"),
                    "shipping_days": it.get("shipping_days"),
                    "url": it.get("url") or it.get("link") or it.get("affiliate_url"),
                    "matched_attributes": it.get("matched_attributes", []),
                })
            return mapped
    except Exception:
        return []


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # try RapidAPI if keys/host are configured
    results = await _call_rapidapi(query, budget)
    if results:
        return results
    # if RapidAPI not configured or returned nothing, return empty to allow
    # the central search service to decide whether to use the sample catalog
    return []


async def search_parsed(parsed_query) -> List[Dict[str, Any]]:
    q = getattr(parsed_query, "q", "")
    budget = getattr(getattr(parsed_query, "constraints", None), "budget", None)
    return await search(q, budget)
