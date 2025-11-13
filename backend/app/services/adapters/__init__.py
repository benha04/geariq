from typing import List, Dict, Any, Union
from .impact import search as impact_search, search as impact_search_parsed
from .cj import search as cj_search, search_parsed as cj_search_parsed
from .rakuten import search as rakuten_search, search_parsed as rakuten_search_parsed


async def fetch_candidates(query_or_parsed: Union[str, object], budget: float | None = None) -> List[Dict[str, Any]]:
    """Call available adapters and return concatenated normalized results.

    Accepts either a raw query string or a ParsedQuery object. Each adapter may
    provide a `search_parsed` function to consume the ParsedQuery.
    """
    results: List[Dict[str, Any]] = []

    # Helper to call adapter functions with either parsed or legacy signature
    async def _call(adapter_search, adapter_search_parsed=None):
        try:
            if adapter_search_parsed and not isinstance(query_or_parsed, str):
                res = await adapter_search_parsed(query_or_parsed)
            elif isinstance(query_or_parsed, str):
                res = await adapter_search(query_or_parsed, budget)
            else:
                # fallback: pass q and budget
                q = getattr(query_or_parsed, "q", str(query_or_parsed))
                b = getattr(query_or_parsed, "constraints", None)
                bval = getattr(b, "budget", None) if b is not None else None
                res = await adapter_search(q, bval)
            if res:
                results.extend(res)
        except Exception:
            # In production, log failures per-adapter
            pass

    # Call Impact
    await _call(impact_search, impact_search_parsed)
    # Call CJ
    await _call(cj_search, cj_search_parsed)
    # Call Rakuten
    await _call(rakuten_search, rakuten_search_parsed)

    return results
