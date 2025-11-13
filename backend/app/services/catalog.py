import json
import os
from pathlib import Path
from typing import List, Dict

_CATALOG: List[Dict] | None = None


def _load_sample_catalog() -> List[Dict]:
    global _CATALOG
    if _CATALOG is not None:
        return _CATALOG
    base = Path(__file__).resolve().parent.parent.parent
    sample_path = Path(os.environ.get("SAMPLE_CATALOG_PATH", base / "data" / "sample_catalog.json"))
    if not sample_path.exists():
        # create a tiny in-repo sample catalog if missing
        sample = [
            {"title": "Acme MIPS Helmet", "retailer": "Acme", "price": 129.99, "rating": 4.5, "shipping_days": 2, "url": "https://acme.example/mips-helmet", "category": "helmet", "attributes": ["mips", "helmet"]},
            {"title": "RoadPro MIPS Helmet", "retailer": "RoadPro", "price": 119.0, "rating": 4.3, "shipping_days": 3, "url": "https://roadpro.example/mips-helmet", "category": "helmet", "attributes": ["mips", "helmet"]},
            {"title": "PowX Snowboard - All Mountain", "retailer": "PowX", "price": 279.0, "rating": 4.6, "shipping_days": 4, "url": "https://powx.example/snowboard", "category": "snowboard", "attributes": ["snowboard"]},
            {"title": "PixelBook Ultra 14", "retailer": "ElectroMart", "price": 1299.0, "rating": 4.7, "shipping_days": 2, "url": "https://electromart.example/pixelbook-ultra-14", "category": "laptop", "attributes": ["laptop", "computer"]},
            {"title": "ProGamer RTX Desktop", "retailer": "ComputeHub", "price": 2199.0, "rating": 4.8, "shipping_days": 5, "url": "https://compute.example/rtx-desktop", "category": "desktop", "attributes": ["desktop", "computer"]},
            {"title": "TrailRunner Mountain Bike", "retailer": "BikeWorld", "price": 849.0, "rating": 4.4, "shipping_days": 6, "url": "https://bikeworld.example/trailrunner", "category": "bike", "attributes": ["bike", "mountain"]},
            {"title": "Studio Headphones ZX", "retailer": "AudioPlus", "price": 249.0, "rating": 4.5, "shipping_days": 2, "url": "https://audioplus.example/zx-headphones", "category": "headphones", "attributes": ["headphones", "audio"]},
            {"title": "Camping 4P Dome Tent", "retailer": "OutGear", "price": 199.0, "rating": 4.1, "shipping_days": 3, "url": "https://outgear.example/4p-dome", "category": "camping", "attributes": ["tent", "camping"]},
        ]
        _CATALOG = sample
        return _CATALOG
    with open(sample_path, "r", encoding="utf-8") as fh:
        _CATALOG = json.load(fh)
    return _CATALOG


def search_catalog(q: str, top_n: int = 10) -> List[Dict]:
    """Simple catalog search: token-match on title/category/attributes.

    This is intentionally lightweight: it gives a development fallback so the API
    can return diverse product types when live marketplace APIs aren't configured.
    """
    qnorm = (q or "").lower().strip()
    if not qnorm:
        return []
    catalog = _load_sample_catalog()
    tokens = [t for t in qnorm.replace("/", " ").split() if t]

    def score_item(item: Dict) -> int:
        s = 0
        title = item.get("title", "").lower()
        cat = (item.get("category") or "").lower()
        attrs = [a.lower() for a in item.get("attributes", [])]
        for t in tokens:
            if t in title:
                s += 10
            if t == cat:
                s += 8
            if t in attrs:
                s += 6
            # partial word match
            if any(t in part for part in [title, cat] + attrs):
                s += 1
        return s

    scored = [(score_item(it), it) for it in catalog]
    scored = [it for it in scored if it[0] > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it[1] for it in scored[:top_n]]
