from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    text: str
    duration_sec: float  # from audio metadata

class CriterionScore(BaseModel):
    name: str
    raw_score: float      
    max_score: float
    normalized: float    
    details: dict

class OverallResponse(BaseModel):
    final_score_0_100: float
    criteria: list[CriterionScore]
