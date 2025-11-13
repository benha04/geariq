from typing import List, Dict, Any
import os
import asyncio
import httpx

from app.core.config import settings
from app.services.catalog import search_catalog


async def _call_impact_api(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Attempt a real HTTP call to the configured Impact API base.

    This function expects environment variables to be set:
    - IMPACT_API_BASE (optional, default is a reasonable placeholder)
    - IMPACT_API_KEY (required)
    - IMPACT_PARTNER_SID (optional)

    If the call fails for any reason, return an empty list to fall back to stubs.
    """
    api_base = os.getenv("IMPACT_API_BASE") or "https://api.impact.com"
    api_key = os.getenv("IMPACT_API_KEY")
    if not api_key:
        return []

    url = f"{api_base}/v1/search"
    params = {"q": query}
    if budget is not None:
        params["budget"] = budget

    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    partner_sid = os.getenv("IMPACT_PARTNER_SID")
    if partner_sid:
        headers["X-Impact-Partner-Sid"] = partner_sid

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            # Expect data to be a list of results or { items: [...] }
            items = data if isinstance(data, list) else data.get("items") or []
            mapped: List[Dict[str, Any]] = []
            for it in items:
                mapped.append({
                    "title": it.get("title"),
                    "retailer": it.get("merchant") or it.get("retailer"),
                    "price": it.get("price"),
                    "rating": it.get("rating"),
                    "shipping_days": it.get("shipping_days"),
                    "url": it.get("url") or it.get("affiliate_url"),
                    "matched_attributes": it.get("matched_attributes", []),
                })
            return mapped
    except Exception:
        # In production we'd log the exception; fall back to catalog for dev
        return []


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # Prefer real API if key is configured; otherwise use catalog fallback for dev.
    key = os.getenv("IMPACT_API_KEY") or settings.openai_api_key
    if key:
        results = await _call_impact_api(query, budget)
        if results:
            return results

    # If Impact is not configured or returned no items, return empty so the
    # central search service can decide whether to fall back to the sample
    # catalog.
    return []


async def search_parsed(parsed_query) -> List[Dict[str, Any]]:
    q = getattr(parsed_query, "q", "")
    budget = getattr(getattr(parsed_query, "constraints", None), "budget", None)
    return await search(q, budget)
