# api/schemas.py
from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    text: str
    duration_sec: float  # from audio metadata

class CriterionScore(BaseModel):
    name: str
    raw_score: float      # rubric-scale score (e.g. 0–5, 0–10, 0–15)
    max_score: float
    normalized: float     # 0–1
    details: dict

class OverallResponse(BaseModel):
    final_score_0_100: float
    criteria: list[CriterionScore]
