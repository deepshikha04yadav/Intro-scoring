import re
from typing import Dict

def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))

def band_from_wpm(wpm: float) -> Dict:
   
    if wpm > 161:
        return {"label": "too_fast", "raw": 2}
    if 141 <= wpm <= 160:
        return {"label": "fast", "raw": 6}
    if 111 <= wpm <= 140:
        return {"label": "ideal", "raw": 10}
    if 81 <= wpm <= 110:
        return {"label": "slow", "raw": 6}
    return {"label": "too_slow", "raw": 2}

def score_speech_rate(text: str, duration_sec: float) -> Dict:
    wc = _word_count(text)
    wpm = wc / duration_sec * 60 if duration_sec > 0 else 0
    band = band_from_wpm(wpm)
    raw = band["raw"] 
    return {
        "raw": raw,
        "max": 10.0,
        "normalized": raw / 10.0,
        "wpm": wpm,
        "band": band["label"],
    }
