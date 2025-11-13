from typing import Dict, Any
from app.db.session import SessionLocal
from app.models.track import Track
from sqlalchemy.exc import SQLAlchemyError

_STORE: Dict[int, Dict[str, Any]] = {}
_ID = 1


def track_rule(rule: Dict[str, Any]) -> Dict[str, Any]:
    """Persist rule to DB if possible, otherwise fall back to in-memory store."""
    # Try DB persistence
    try:
        db = SessionLocal()
        tr = Track(q=rule.get("q"), budget=rule.get("budget"), contact=rule.get("contact"))
        db.add(tr)
        db.commit()
        db.refresh(tr)
        return {"id": tr.id, "q": tr.q, "budget": tr.budget, "contact": tr.contact}
    except SQLAlchemyError:
        # fallback to in-memory
        global _ID
        rid = _ID
        _ID += 1
        rule_copy = dict(rule)
        rule_copy["id"] = rid
        _STORE[rid] = rule_copy
        return rule_copy


def list_rules():
    try:
        db = SessionLocal()
        return [ {"id": r.id, "q": r.q, "budget": r.budget, "contact": r.contact} for r in db.query(Track).all() ]
    except SQLAlchemyError:
        return list(_STORE.values())
