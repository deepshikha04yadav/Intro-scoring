from typing import Dict
import re

FILLERS = [
    "um", "uh", "like", "you know", "so", "actually", "basically",
    "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah",
]

def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))

def score_clarity(text: str) -> Dict:
    text_lower = text.lower()
    filler_count = 0
    for f in FILLERS:
        filler_count += text_lower.count(f)

    wc = _word_count(text)
    rate = (filler_count / wc * 100) if wc > 0 else 0

    # Map rate to rubric scores 0–15
    if 0 <= rate <= 3:
        raw = 15
    elif 4 <= rate <= 6:
        raw = 12
    elif 7 <= rate <= 9:
        raw = 9
    elif 10 <= rate <= 12:
        raw = 6
    else:
        raw = 3

    return {
        "raw": raw,
        "max": 15.0,
        "normalized": raw / 15.0,
        "filler_count": filler_count,
        "filler_rate": rate,
    }
