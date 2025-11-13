from typing import List, Dict, Any, Union
from app.services.adapters import fetch_candidates
from app.services.cache import make_key, get as cache_get, set as cache_set
from app.api.schemas.search import ParsedQuery
from app.services.catalog import search_catalog


async def search_marketplaces(query_or_parsed: Union[str, ParsedQuery], budget: float | None = None) -> List[Dict[str, Any]]:
    """Fetch product candidates from registered adapters.

    Backwards-compatible: accepts either (q: str, budget: float) or a ParsedQuery instance.
    """
    # Normalize to parsed query for internal processing
    if isinstance(query_or_parsed, ParsedQuery):
        parsed_query = query_or_parsed
    else:
        # legacy call (q, budget)
        parsed_query = ParsedQuery(q=str(query_or_parsed))
        if budget is not None:
            parsed_query.constraints.budget = budget

    # Try cache first (short TTL)
    cache_key = make_key(parsed_query)
    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    # call adapters - some adapters may accept a ParsedQuery, others expect (q, budget)
    try:
        candidates = await fetch_candidates(parsed_query)
    except TypeError:
        # fallback to legacy adapter signature
        candidates = await fetch_candidates(parsed_query.q, parsed_query.constraints.budget)

    # If adapters returned nothing, use the sample catalog fallback so the
    # API can still return diverse product types during development.
    if not candidates:
        candidates = search_catalog(parsed_query.q or "", top_n=10)

    # adapters are expected to return normalized dicts; ensure budget filtering as a safeguard
    budget_val = parsed_query.constraints.budget
    if budget_val is not None:
        filtered: List[Dict[str, Any]] = []
        for d in candidates:
            price_val = d.get("price", 0.0)
            if isinstance(price_val, (int, float)):
                price_f = float(price_val)
            elif isinstance(price_val, str):
                try:
                    price_f = float(price_val)
                except ValueError:
                    price_f = 0.0
            else:
                price_f = 0.0

            if price_f <= budget_val:
                filtered.append(d)

        candidates = filtered

    # Category / attribute filtering: if parser detected a category (e.g., 'helmet'),
    # prefer candidates that mention the category in title or matched_attributes.
    cat = getattr(parsed_query, 'category', None)
    attrs = getattr(parsed_query, 'attributes', []) or []
    if cat or attrs:
        cat_tokens = set()
        if cat:
            cat_tokens.add(cat.lower().rstrip('s'))
            cat_tokens.add(cat.lower())
        for a in attrs:
            cat_tokens.add(a.lower())

        def matches_category(d: dict) -> bool:
            title = (d.get('title') or '').lower()
            mat = [m.lower() for m in d.get('matched_attributes', []) if isinstance(m, str)]
            # match if any token appears in title or matched_attributes
            for t in cat_tokens:
                if t and (t in title or t in mat):
                    return True
            return False

        filtered2 = [c for c in candidates if matches_category(c)]
        # if we found matches, restrict to them; otherwise keep original candidates
        if filtered2:
            candidates = filtered2

    # store in cache for 120s
    try:
        cache_set(cache_key, candidates, ttl=120)
    except Exception:
        pass

    return candidates
