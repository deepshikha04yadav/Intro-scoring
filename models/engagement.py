# models/engagement.py
from typing import Dict
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def score_engagement(text: str) -> Dict:
    scores = sia.polarity_scores(text)
    pos_prob = scores["pos"]  # 0–1[attached_file:8cf2f828-ba64-496c-88f2-5596011ec523]

    if pos_prob >= 0.9:
        raw = 15
    elif pos_prob >= 0.7:
        raw = 12
    elif pos_prob >= 0.5:
        raw = 9
    elif pos_prob >= 0.3:
        raw = 6
    else:
        raw = 3

    return {
        "raw": raw,
        "max": 15.0,
        "normalized": raw / 15.0,
        "pos_prob": pos_prob,
        "sentiment_scores": scores,
    }
