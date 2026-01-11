from fastmcp import FastMCP
from langdetect import detect
from textblob import TextBlob

mcp = FastMCP("hotel-review-processor")

@mcp.tool()
def analyze_review(text: str) -> dict:
    """
    Analyze a hotel review and extract language, sentiment and aspects.
    """

    try:
        language = detect(text)
    except Exception:
        language = "unknown"

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    aspects = []
    keywords = {
        "cleanliness": ["clean", "dirty", "limpio", "sucio"],
        "service": ["staff", "service", "personal", "servicio"],
        "room": ["room", "habitación"],
        "food": ["food", "breakfast", "comida", "desayuno"],
        "noise": ["noise", "ruido"],
        "location": ["location", "ubicación"]
    }

    lower = text.lower()
    for aspect, words in keywords.items():
        if any(w in lower for w in words):
            aspects.append(aspect)

    return {
        "language": language,
        "sentiment": sentiment,
        "aspects": aspects
    }
