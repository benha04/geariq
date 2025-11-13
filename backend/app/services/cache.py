import time
from typing import Any, Optional
import os

_STORE: dict[str, tuple[float, Any]] = {}
_REDIS = None
_USE_REDIS = False
if os.getenv("REDIS_URL"):
    try:
        import redis

        _REDIS = redis.from_url(os.getenv("REDIS_URL"))
        _USE_REDIS = True
    except Exception:
        _REDIS = None
        _USE_REDIS = False


def make_key(obj) -> str:
    q = getattr(obj, "q", str(obj))
    attrs = getattr(obj, "attributes", [])
    constraints = getattr(obj, "constraints", None)
    budget = getattr(constraints, "budget", None) if constraints is not None else None
    in_stock = getattr(constraints, "in_stock", None) if constraints is not None else None
    ship = getattr(constraints, "ship_by_days", None) if constraints is not None else None
    min_rating = getattr(constraints, "min_rating", None) if constraints is not None else None
    parts = [str(q), ",".join(sorted(attrs)), f"b={budget}", f"in_stock={in_stock}", f"ship={ship}", f"rating={min_rating}"]
    key = "|".join(parts)
    return key


def get(key: str) -> Optional[Any]:
    if _USE_REDIS and _REDIS:
        try:
            raw = _REDIS.get(key)
            if not raw:
                return None
            import pickle

            return pickle.loads(raw)
        except Exception:
            return None

    v = _STORE.get(key)
    if not v:
        return None
    expires_at, value = v
    if time.time() > expires_at:
        del _STORE[key]
        return None
    return value


def set(key: str, value: Any, ttl: int = 300):
    if _USE_REDIS and _REDIS:
        try:
            import pickle

            _REDIS.set(name=key, value=pickle.dumps(value), ex=ttl)
            return
        except Exception:
            pass

    _STORE[key] = (time.time() + ttl, value)
