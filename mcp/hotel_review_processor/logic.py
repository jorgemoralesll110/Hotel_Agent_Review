from __future__ import annotations

from typing import Dict, List

from langdetect import detect
from textblob import TextBlob


ASPECT_KEYWORDS = {
    "cleanliness": ["clean", "dirty", "hygiene", "smell", "stain", "mold", "mould"],
    "staff": ["staff", "rude", "friendly", "helpful", "reception", "service"],
    "noise": ["noise", "noisy", "loud", "quiet", "thin walls", "party"],
    "location": ["location", "distance", "near", "far", "metro", "beach", "center", "centre"],
    "room": ["room", "bed", "pillow", "bathroom", "shower", "air conditioning", "ac"],
    "food": ["breakfast", "food", "buffet", "restaurant", "dinner"],
    "price": ["price", "expensive", "cheap", "value", "worth"],
}


def _detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"


def _sentiment_polarity(text: str) -> float:
    try:
        return float(TextBlob(text).sentiment.polarity)
    except Exception:
        return 0.0


def _extract_aspects(text: str) -> List[str]:
    lowered = text.lower()
    found = []
    for aspect, kws in ASPECT_KEYWORDS.items():
        if any(kw in lowered for kw in kws):
            found.append(aspect)
    return found


def analyze_review(text: str) -> Dict:
    lang = _detect_language(text)
    polarity = _sentiment_polarity(text)
    aspects = _extract_aspects(text)

    if polarity <= -0.4:
        sentiment = "very_negative"
    elif polarity <= -0.1:
        sentiment = "negative"
    elif polarity < 0.1:
        sentiment = "neutral"
    elif polarity < 0.4:
        sentiment = "positive"
    else:
        sentiment = "very_positive"

    severity = "low"
    if sentiment in {"negative", "very_negative"} and len(aspects) >= 2:
        severity = "high"
    elif sentiment in {"negative", "very_negative"} and len(aspects) >= 1:
        severity = "medium"
    elif sentiment in {"neutral"} and len(aspects) >= 2:
        severity = "medium"

    return {
        "language": lang,
        "polarity": polarity,
        "sentiment": sentiment,
        "aspects": aspects,
        "severity": severity,
    }
