from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services.search_service import search_marketplaces
from app.services.matching import pick_best

router = APIRouter()

class SearchResponse(BaseModel):
    best: dict | None
    candidates: list[dict]

@router.get("/search", response_model=SearchResponse)
async def search(q: str = Query(..., description="e.g., 'MIPS bike helmet'"), budget: float | None = Query(None)):
    candidates = await search_marketplaces(q, budget)
    best = pick_best(candidates)
    return {"best": best, "candidates": candidates}
