from langdetect import detect
from textblob import TextBlob

def analyze_review(text: str):
    # Idioma
    try:
        language = detect(text)
    except Exception:
        language = "unknown"

    # Sentimiento
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Aspectos
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
