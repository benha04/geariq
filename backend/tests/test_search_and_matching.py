import asyncio

from app.services.search_service import search_marketplaces
from app.services.matching import pick_best


def test_search_happy_path():
    # run the async search_marketplaces which currently returns stubbed Impact results
    results = asyncio.get_event_loop().run_until_complete(search_marketplaces("helmet", None))
    assert isinstance(results, list)
    assert len(results) >= 1


def test_search_budget_filter():
    results = asyncio.get_event_loop().run_until_complete(search_marketplaces("helmet", 120.0))
    # all returned prices should be <= 120.0
    for r in results:
        assert float(r.get("price", 0)) <= 120.0


def test_pick_best():
    candidates = [
        {"title": "A", "price": 100.0, "rating": 4.5, "shipping_days": 2},
        {"title": "B", "price": 90.0, "rating": 4.0, "shipping_days": 3},
    ]
    best = pick_best(candidates)
    assert best is not None
    assert best.get("title") in {"A", "B"}
