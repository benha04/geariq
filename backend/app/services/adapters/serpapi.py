import os
import logging
from typing import List, Dict, Any
import httpx

from app.services.catalog import search_catalog
from app.services import cache as _cache


async def _call_serpapi(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Call SerpApi (https://serpapi.com) to fetch shopping results.

    Expects SERPAPI_KEY in env. Optionally SERPAPI_BASE (defaults to https://serpapi.com).
    Uses the `engine=google_shopping` endpoint to retrieve shopping results when
    available. On error or missing key, returns an empty list so callers fall back
    to the sample catalog.
    """
    key = os.getenv("SERPAPI_KEY")
    logger = logging.getLogger(__name__)
    if not key:
        logger.info("serpapi: SERPAPI_KEY not set; skipping SerpApi call")
        return []
    else:
        logger.info("serpapi: SERPAPI_KEY present (redacted)")

    base = os.getenv("SERPAPI_BASE") or "https://serpapi.com"
    url = f"{base}/search.json"
    params = {"engine": "google_shopping", "q": query, "api_key": key}
    # SerpApi supports many other params (gl, hl, location, etc.) — add as needed.
    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            # shopping results commonly live in 'shopping_results'
            items = data.get("shopping_results") or data.get("inline_shopping_results") or []
            logger.info(f"serpapi: fetched {len(items)} shopping results for query='{query}'")
            mapped: List[Dict[str, Any]] = []
            for it in items:
                # SerpApi fields vary; normalize defensively
                title = it.get("title") or it.get("product_title") or it.get("name") or ""
                # Normalize price to float when possible; keep original string if not
                price_val = None
                raw_price = None
                if isinstance(it.get("price"), dict):
                    raw_price = it["price"].get("raw") or it["price"].get("value")
                else:
                    raw_price = it.get("price") or it.get("extracted_price") or it.get("extracted_price_range")

                if isinstance(raw_price, (int, float)):
                    price_val = float(raw_price)
                elif isinstance(raw_price, str):
                    # strip currency symbols and commas
                    import re

                    m = re.search(r"([0-9,.]+)", raw_price)
                    if m:
                        num = m.group(1).replace(",", "")
                        try:
                            price_val = float(num)
                        except Exception:
                            price_val = raw_price
                    else:
                        price_val = raw_price

                # image/thumbnail best-effort fields
                # prefer serpapi's proxied thumbnail when available, otherwise fallback to provider thumbnail
                image = it.get("serpapi_thumbnail") or it.get("thumbnail") or it.get("thumbnail_src") or it.get("image") or it.get("thumbnail_link") or None

                mapped.append({
                    "title": title,
                    "retailer": it.get("source") or it.get("merchant") or it.get("store"),
                    "price": price_val,
                    "rating": it.get("rating") or it.get("reviews") or None,
                    "shipping_days": None,
                    "url": it.get("link") or it.get("product_link") or it.get("shopping_url"),
                    "image": image,
                    "matched_attributes": it.get("attributes", []),
                })
            return mapped
    except Exception:
        return []


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # Use cache to avoid repeated calls and conserve SerpApi quota
    cache_key = f"serpapi|{query}|b={budget}"
    cached = _cache.get(cache_key)
    if cached is not None:
        return cached

    results = await _call_serpapi(query, budget)
    if results:
        # cache results for short TTL
        _cache.set(cache_key, results, ttl=300)
        return results
    # if SerpApi returned nothing, return empty list and let the central
    # search service decide whether to fall back to the sample catalog.
    return []


async def search_parsed(parsed_query) -> List[Dict[str, Any]]:
    q = getattr(parsed_query, "q", "")
    budget = getattr(getattr(parsed_query, "constraints", None), "budget", None)
    return await search(q, budget)
