from typing import List, Dict, Any


def semantic_match(query_text: str, candidates: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
    """Placeholder semantic matching: simple keyword overlap score and return top_k candidates.

In production this would call pgvector or an external vector DB.
"""
    q_tokens = set(query_text.lower().split())
    scored = []
    for c in candidates:
        title = c.get("title", "").lower()
        t_tokens = set(title.split())
        overlap = len(q_tokens & t_tokens)
        scored.append((overlap, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]

