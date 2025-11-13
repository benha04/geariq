from typing import List, Dict, Any, Union
import logging
from .impact import search as impact_search, search as impact_search_parsed
from .cj import search as cj_search, search_parsed as cj_search_parsed
from .rakuten import search as rakuten_search, search_parsed as rakuten_search_parsed
from .rapidapi import search as rapidapi_search, search_parsed as rapidapi_search_parsed
from .scrapeless import search as scrapeless_search, search_parsed as scrapeless_search_parsed
from .serpapi import search as serpapi_search, search_parsed as serpapi_search_parsed

logger = logging.getLogger(__name__)


async def fetch_candidates(query_or_parsed: Union[str, object], budget: float | None = None) -> List[Dict[str, Any]]:
    """Call available adapters and return concatenated normalized results.

    Accepts either a raw query string or a ParsedQuery object. Each adapter may
    provide a `search_parsed` function to consume the ParsedQuery.
    """
    results: List[Dict[str, Any]] = []

    # Helper to call adapter functions with either parsed or legacy signature
    async def _call(adapter_name: str, adapter_search, adapter_search_parsed=None):
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
                try:
                    logger.info(f"adapter:{adapter_name} returned {len(res)} items")
                except Exception:
                    logger.info(f"adapter:{adapter_name} returned items")
        except Exception as e:
            # log adapter failure for easier debugging in dev
            logger.exception(f"adapter:{adapter_name} failed: {e}")

    # Call Impact
    await _call("impact", impact_search, impact_search_parsed)
    # Call SerpApi early to prefer live shopping results
    await _call("serpapi", serpapi_search, serpapi_search_parsed)
    # Call CJ
    await _call("cj", cj_search, cj_search_parsed)
    # Call Rakuten
    await _call("rakuten", rakuten_search, rakuten_search_parsed)
    # Call RapidAPI
    await _call("rapidapi", rapidapi_search, rapidapi_search_parsed)
    # Call Scrapeless
    await _call("scrapeless", scrapeless_search, scrapeless_search_parsed)

    return results
