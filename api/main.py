from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .schemas import TranscriptRequest, CriterionScore, OverallResponse
from models.overall_scorer import score_transcript

app = FastAPI(title="Spoken Intro Scoring API")

origins = [
    "http://localhost:3000", 
    "https://intro-scoring.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],    # Allow POST, GET, OPTIONS etc.
    allow_headers=["*"],    # Allow JSON content-type
)


@app.post("/score", response_model=OverallResponse)
def score_endpoint(req: TranscriptRequest):
    result = score_transcript(req.text, req.duration_sec)
    d = result["detail"]

    criteria = [
        CriterionScore(
            name="Content & Structure",
            raw_score=d["content_structure"]["raw_total"],
            max_score=d["content_structure"]["max_total"],
            normalized=d["content_structure"]["normalized"],
            details=d["content_structure"],
        ),
        CriterionScore(
            name="Speech Rate",
            raw_score=d["speech_rate"]["raw"],
            max_score=d["speech_rate"]["max"],
            normalized=d["speech_rate"]["normalized"],
            details=d["speech_rate"],
        ),
        CriterionScore(
            name="Language & Grammar",
            raw_score=d["language_grammar"]["raw_total"],
            max_score=d["language_grammar"]["max_total"],
            normalized=d["language_grammar"]["normalized"],
            details=d["language_grammar"],
        ),
        CriterionScore(
            name="Clarity",
            raw_score=d["clarity"]["raw"],
            max_score=d["clarity"]["max"],
            normalized=d["clarity"]["normalized"],
            details=d["clarity"],
        ),
        CriterionScore(
            name="Engagement",
            raw_score=d["engagement"]["raw"],
            max_score=d["engagement"]["max"],
            normalized=d["engagement"]["normalized"],
            details=d["engagement"],
        ),
    ]

    return OverallResponse(
        final_score_0_100=result["final_score_0_100"],
        criteria=criteria,
    )
