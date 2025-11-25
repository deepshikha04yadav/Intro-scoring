from typing import Dict
import re
import nltk
import os

nltk.download('vader_lexicon')

nltk.data.path.append(os.path.join(os.path.dirname(__file__), "..", "nltk_data"))
from nltk.tokenize import sent_tokenize


RUBRIC_SCORES = {
    "salutation": {"none": 0, "normal": 2, "good": 4, "excellent": 5},
    "keywords": {"must_have_per_item": 4, "good_to_have_per_item": 2, "max": 30},
    "flow": {"order_followed": 5, "order_not_followed": 0},
}


def score_salutation(text: str) -> Dict:
    text_lower = text.lower()

    if not re.search(r"\bhi\b|\bhello\b|\bgood\s+(morning|afternoon|evening|day)\b", text_lower):
        level = "none"
    elif "excited" in text_lower or "feeling great" in text_lower:
        level = "excellent"
    elif any(x in text_lower for x in ["good morning", "good afternoon", "good evening", "hello everyone"]):
        level = "good"
    else:
        level = "normal"

    raw = RUBRIC_SCORES["salutation"][level]

    return {
        "raw": raw,
        "max": 5.0,
        "normalized": raw / 5.0,
        "level": level,
    }


def score_keywords(text: str) -> Dict:
    text_lower = text.lower()

    must_have = {
        "name": ["my name", "myself"],
        "age": ["years old"],
        "school_class": ["school", "class"],
        "family": ["family"],
        "hobby": ["hobby", "hobbies", "enjoy", "like to", "playing"],
    }

    good_to_have = {
        "family_detail": ["mother", "father", "parents", "sister", "brother"],
        "origin": ["i am from"],
        "goal": ["goal", "dream", "ambition"],
        "fun_fact": ["fun fact", "something unique", "one thing people don't know"],
        "strengths": ["achievement", "strength", "proud of"],
    }

    must_score = sum(
        RUBRIC_SCORES["keywords"]["must_have_per_item"]
        for _, pats in must_have.items()
        if any(p in text_lower for p in pats)
    )

    good_score = sum(
        RUBRIC_SCORES["keywords"]["good_to_have_per_item"]
        for _, pats in good_to_have.items()
        if any(p in text_lower for p in pats)
    )

    raw = min(must_score + good_score, RUBRIC_SCORES["keywords"]["max"])

    return {
        "raw": raw,
        "max": 30.0,
        "normalized": raw / 30.0,
        "must_score": must_score,
        "good_score": good_score,
    }


def score_flow(text: str) -> Dict:
    sentences = sent_tokenize(text)
    first = sentences[0].lower() if sentences else ""
    last = sentences[-1].lower() if sentences else ""

    has_salutation = any(word in first for word in ["hello", "good", "hi"])
    has_closing = any(word in last for word in ["thank you", "thanks"])

    if has_salutation and has_closing:
        raw = RUBRIC_SCORES["flow"]["order_followed"]
        order = "order_followed"
    else:
        raw = RUBRIC_SCORES["flow"]["order_not_followed"]
        order = "order_not_followed"

    return {
        "raw": raw,
        "max": 5.0,
        "normalized": raw / 5.0,
        "order": order,
    }


def score_content_structure(text: str) -> Dict:
    sal = score_salutation(text)
    kw = score_keywords(text)
    fl = score_flow(text)

    total_raw = sal["raw"] + kw["raw"] + fl["raw"]

    return {
        "salutation": sal,
        "keywords": kw,
        "flow": fl,
        "raw_total": total_raw,
        "max_total": 40.0,
        "normalized": total_raw / 40.0,
    }
