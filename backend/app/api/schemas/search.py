from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Constraint(BaseModel):
    budget: Optional[float] = None
    ship_by_days: Optional[int] = None
    min_rating: Optional[float] = None
    in_stock: Optional[bool] = None


class Preference(BaseModel):
    brand: Optional[str] = None


class ParsedQuery(BaseModel):
    q: str
    category: Optional[str] = None
    attributes: List[str] = Field(default_factory=list)
    constraints: Constraint = Field(default_factory=Constraint)
    preferences: Preference = Field(default_factory=Preference)


class ScoreBreakdown(BaseModel):
    price: float
    rating: float
    shipping: float
    total: float


class Candidate(BaseModel):
    title: str
    url: Optional[str]
    price: Optional[float]
    rating: Optional[float]
    shipping_days: Optional[int]
    retailer: Optional[str]
    matched_attributes: List[str] = Field(default_factory=list)
    score_breakdown: Optional[ScoreBreakdown] = None


class Rationale(BaseModel):
    matched_features: List[str] = Field(default_factory=list)
    score_breakdown: Optional[ScoreBreakdown] = None
    why: Optional[str] = None


class SearchResponse(BaseModel):
    best: Optional[Candidate]
    candidates: List[Candidate]
    rationale: Optional[Rationale]
