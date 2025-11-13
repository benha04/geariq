import re
from typing import List
from app.api.schemas.search import ParsedQuery


_price_re = re.compile(r"(?:under|<=|<|less than|budget)\s*\$?(\d+(?:\.\d+)?)", re.I)
_price_re2 = re.compile(r"\$\s*(\d+(?:\.\d+)?)")
_ship_re = re.compile(r"(\d+)[- ]?\s*(?:day|days|d)\b", re.I)
_ship_phrase_re = re.compile(r"(\d+)[- ]?\s*(?:day|days) delivery|within (\d+) days", re.I)
_rating_re = re.compile(r"(\d(?:\.\d)?)\s*\+?\s*(?:stars|star|rating)", re.I)
_condition_re = re.compile(r"\b(new|used|refurbished)\b", re.I)
_in_stock_re = re.compile(r"\b(in stock|available|instock)\b", re.I)
_exclude_re = re.compile(r"(?:exclude|except|not)\s+([A-Za-z0-9]+)", re.I)
_min_reviews_re = re.compile(r"(\d+)\s*(?:reviews|review|ratings)\b", re.I)


def parse(q: str) -> ParsedQuery:
    pq = ParsedQuery(q=q)

    # budget
    m = _price_re.search(q)
    if m:
        try:
            pq.constraints.budget = float(m.group(1))
        except Exception:
            pass
    else:
        # fallback: first $number in query
        m2 = _price_re2.search(q)
        if m2:
            try:
                pq.constraints.budget = float(m2.group(1))
            except Exception:
                pass

    # shipping days
    m = _ship_phrase_re.search(q)
    if m:
        days = m.group(1) or m.group(2)
        try:
            pq.constraints.ship_by_days = int(days)
        except Exception:
            pass
    else:
        m2 = _ship_re.search(q)
        if m2:
            try:
                pq.constraints.ship_by_days = int(m2.group(1))
            except Exception:
                pass

    # min rating
    m = _rating_re.search(q)
    if m:
        try:
            pq.constraints.min_rating = float(m.group(1))
        except Exception:
            pass

    # condition
    m = _condition_re.search(q)
    if m:
        cond = m.group(1).lower()
        # store condition as an attribute for now
        pq.attributes.append(cond)

    # in-stock hint
    if _in_stock_re.search(q):
        pq.constraints.in_stock = True

    # exclude tokens
    excl = _exclude_re.findall(q)
    if excl:
        # store excluded values in attributes prefixed with 'exclude:' to be handled downstream
        for e in excl:
            pq.attributes.append(f"exclude:{e}")

    # min review count
    m = _min_reviews_re.search(q)
    if m:
        try:
            pq.preferences.__dict__["min_review_count"] = int(m.group(1))
        except Exception:
            pass

    # simple attribute extraction: look for known tokens (MIPS, carbon, wireless, etc.)
    tokens = re.findall(r"\b([A-Za-z0-9+-]{2,})\b", q)
    for t in tokens:
        tl = t.lower()
        if tl in {"mips", "carbon", "wireless", "wide", "wide-angle", "wideangle", "50mm", "lens", "helmet", "snowboard"}:
            pq.attributes.append(t)

    # dedupe attributes while preserving order
    seen = set()
    deduped: List[str] = []
    for a in pq.attributes:
        if a not in seen:
            seen.add(a)
            deduped.append(a)
    pq.attributes = deduped

    # category heuristics with synonyms
    ql = q.lower()
    if "helmet" in ql:
        pq.category = "helmet"
    elif "lens" in ql or "50mm" in ql:
        pq.category = "lens"
    else:
        # synonyms mapping
        if any(tok in ql for tok in ["snowboard", "snowboarding", "snowboarder"]):
            pq.category = "snowboard"
        elif any(tok in ql for tok in ["bike", "bicycle", "cycling"]):
            pq.category = "bike"

    # brand simple rule: look for 'brand=Giro' or 'Giro'
    m = re.search(r"brand\s*[=:\-]?\s*([A-Za-z0-9]+)", q, re.I)
    if m:
        pq.preferences.brand = m.group(1)
    else:
        # first capitalized token could be brand (naive)
        cap = re.findall(r"\b([A-Z][a-z0-9]{1,})\b", q)
        if cap:
            pq.preferences.brand = cap[0]

    return pq
