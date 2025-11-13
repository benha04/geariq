from fastapi import APIRouter, Query
from app.services.search_service import search_marketplaces
from app.services.matching import pick_best
from app.services.query_parser import parse as parse_query
from app.api.schemas.search import SearchResponse, ParsedQuery
from fastapi import HTTPException

from app.api import schemas as api_schemas
from app.services.track import track_rule
from app.services.adapters import impact as impact_adapter


router = APIRouter()


@router.get("/search", response_model=SearchResponse)
async def search(q: str = Query(..., description="e.g., 'MIPS bike helmet'"), budget: float | None = Query(None)):
    # parse free-text into structured query
    parsed: ParsedQuery = parse_query(q)
    # override budget if provided explicitly
    if budget is not None:
        parsed.constraints.budget = budget

    candidates = await search_marketplaces(parsed)
    best = pick_best(candidates)
    # build a richer rationale if best exists
    rationale = None
    if best is not None:
        sb = best.get("score_breakdown") or {}
        # add price vs median heuristic
        prices = [c.get("price") for c in candidates if isinstance(c.get("price"), (int, float))]
        median_price = None
        if prices:
            prices_sorted = sorted(prices)
            mid = len(prices_sorted) // 2
            median_price = prices_sorted[mid]
        why = "Weighted score using price, rating, shipping (higher is better)."
        if median_price is not None and best.get("price") is not None:
            if best.get("price") < median_price:
                why = f"Better than median price (${median_price}) and matches key features."
            else:
                why = f"Competitive on features; price is ${best.get('price')} vs median ${median_price}."
        rationale = {"matched_features": best.get("matched_attributes", []), "score_breakdown": sb, "why": why}
    return {"best": best, "candidates": candidates, "rationale": rationale}



@router.post("/track")
async def track(rule: dict):
    """Simple stub to register a tracking rule. Expects JSON like {q, budget, contact}.

    Currently this stores the rule in-memory for demo purposes.
    """
    if not rule.get("q"):
        raise HTTPException(status_code=400, detail="Missing 'q' in rule")
    stored = track_rule(rule)
    return {"status": "ok", "id": stored["id"]}


@router.get("/admin/verify-impact")
async def verify_impact():
    """Verify Impact credentials by attempting a light search call.

    Returns {ok: true} on success and error detail on failure.
    """
    # Use a harmless query to verify credentials
    try:
        res = await impact_adapter.search_parsed(ParsedQuery(q="test"))
        if res:
            return {"ok": True, "samples": len(res)}
        return {"ok": True, "samples": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/admin/tracks')
async def list_tracks():
    """Return persisted track rules (DB or in-memory fallback)."""
    from app.services.track import list_rules

    return {"rules": list_rules()}
