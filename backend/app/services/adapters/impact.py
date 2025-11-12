from typing import List, Dict, Any
import os
import asyncio

from app.core.config import settings


async def _call_impact_api(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    """Placeholder: real HTTP call to Impact API would go here using httpx.

    For now, return an empty list to indicate no remote data.
    """
    await asyncio.sleep(0)  # keep function async
    return []


def _stubbed_results() -> List[Dict[str, Any]]:
    return [
        {"title": "Acme MIPS Helmet (Impact)", "retailer": "ImpactMall", "price": 129.99, "rating": 4.6, "shipping_days": 2, "url": "https://impact.example/irei"},
        {"title": "RoadPro MIPS Helmet (Impact)", "retailer": "ImpactStore", "price": 119.0, "rating": 4.4, "shipping_days": 2, "url": "https://impact.example/amazon"},
    ]


async def search(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    # If an API key is configured, a real call would be made; otherwise return stubs.
    key = os.getenv("IMPACT_API_KEY") or settings.openai_api_key  # reuse env if present
    if not key:
        return _stubbed_results()

    # TODO: implement real API call with httpx and map fields to normalized shape.
    return await _call_impact_api(query, budget)
