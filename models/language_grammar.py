# # models/language_grammar.py
# from typing import Dict
# import language_tool_python
# import re

# tool = language_tool_python.LanguageTool(
#     "en-US",
#     remote_server="https://api.languagetool.org/v2/check"
# )

# def _word_count(text: str) -> int:
#     return len(re.findall(r"\w+", text))

# def score_grammar(text: str) -> Dict:
#     matches = tool.check(text)
#     wc = _word_count(text)
#     errors_per_100 = (len(matches) / wc * 100) if wc > 0 else 0
#     grammar_score = 1 - min(errors_per_100 / 10, 1)  # rubric formula[attached_file:8cf2f828-ba64-496c-88f2-5596011ec523]

#     # Map grammar_score (0–1) to rubric bands 0–10
#     if grammar_score > 0.9:
#         raw = 10
#     elif grammar_score >= 0.7:
#         raw = 8
#     elif grammar_score >= 0.5:
#         raw = 6
#     elif grammar_score >= 0.3:
#         raw = 4
#     else:
#         raw = 2

#     return {
#         "raw": raw,
#         "max": 10.0,
#         "normalized": raw / 10.0,
#         "errors": len(matches),
#         "errors_per_100": errors_per_100,
#         "grammar_score": grammar_score,
#     }

# def score_vocabulary_ttr(text: str) -> Dict:
#     tokens = re.findall(r"\w+", text.lower())
#     wc = len(tokens)
#     distinct = len(set(tokens))
#     ttr = distinct / wc if wc > 0 else 0

#     if 0.9 <= ttr <= 1.0:
#         raw = 10
#     elif 0.7 <= ttr < 0.9:
#         raw = 8
#     elif 0.5 <= ttr < 0.7:
#         raw = 6
#     elif 0.3 <= ttr < 0.5:
#         raw = 4
#     else:
#         raw = 2    #[attached_file:8cf2f828-ba64-496c-88f2-5596011ec523]

#     return {
#         "raw": raw,
#         "max": 10.0,
#         "normalized": raw / 10.0,
#         "ttr": ttr,
#     }

# def score_language_grammar(text: str) -> Dict:
#     gram = score_grammar(text)
#     vocab = score_vocabulary_ttr(text)
#     total_raw = gram["raw"] + vocab["raw"]  # max 20[attached_file:8cf2f828-ba64-496c-88f2-5596011ec523]
#     return {
#         "grammar": gram,
#         "vocab": vocab,
#         "raw_total": total_raw,
#         "max_total": 20.0,
#         "normalized": total_raw / 20.0,
#     }

# models/language_grammar.py
from typing import Dict
from spellchecker import SpellChecker
import re

spell = SpellChecker()

def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))

def score_grammar(text: str) -> Dict:
    # Tokenize: extract only alphabetical words
    tokens = re.findall(r"[A-Za-z]+", text.lower())
    wc = len(tokens)

    # Find spelling errors
    errors = spell.unknown(tokens)
    error_count = len(errors)

    errors_per_100 = (error_count / wc * 100) if wc > 0 else 0

    # Score logic (same structure as original)
    grammar_score = 1 - min(errors_per_100 / 10, 1)

    # Map grammar_score to rubric score 0–10
    if grammar_score > 0.9:
        raw = 10
    elif grammar_score >= 0.7:
        raw = 8
    elif grammar_score >= 0.5:
        raw = 6
    elif grammar_score >= 0.3:
        raw = 4
    else:
        raw = 2

    return {
        "raw": raw,
        "max": 10.0,
        "normalized": raw / 10.0,
        "errors": error_count,
        "errors_per_100": errors_per_100,
        "misspelled_words": list(errors),
        "grammar_score": grammar_score,
    }

def score_vocabulary_ttr(text: str) -> Dict:
    tokens = re.findall(r"\w+", text.lower())
    wc = len(tokens)
    distinct = len(set(tokens))
    ttr = distinct / wc if wc > 0 else 0

    if 0.9 <= ttr <= 1.0:
        raw = 10
    elif 0.7 <= ttr < 0.9:
        raw = 8
    elif 0.5 <= ttr < 0.7:
        raw = 6
    elif 0.3 <= ttr < 0.5:
        raw = 4
    else:
        raw = 2

    return {
        "raw": raw,
        "max": 10.0,
        "normalized": raw / 10.0,
        "ttr": ttr,
    }

def score_language_grammar(text: str) -> Dict:
    gram = score_grammar(text)
    vocab = score_vocabulary_ttr(text)
    total_raw = gram["raw"] + vocab["raw"]  # max 20

    return {
        "grammar": gram,
        "vocab": vocab,
        "raw_total": total_raw,
        "max_total": 20.0,
        "normalized": total_raw / 20.0,
    }
