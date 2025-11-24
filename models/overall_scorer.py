from typing import Dict
from models.content_structure import score_content_structure
from models.speech_rate import score_speech_rate
from models.language_grammar import score_language_grammar
from models.clarity import score_clarity
from models.engagement import score_engagement

def score_transcript(text: str, duration_sec: float) -> Dict:
    cs = score_content_structure(text)
    sr = score_speech_rate(text, duration_sec)
    lg = score_language_grammar(text)
    cl = score_clarity(text)
    en = score_engagement(text)


    final_raw = cs["raw_total"] + sr["raw"] + lg["raw_total"] + cl["raw"] + en["raw"]

    return {
        "final_score_0_100": final_raw,
        "detail": {
            "content_structure": cs,
            "speech_rate": sr,
            "language_grammar": lg,
            "clarity": cl,
            "engagement": en,
        },
    }
