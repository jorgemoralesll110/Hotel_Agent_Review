def extract_aspects(text: str):
    aspects = []
    keywords = {
        "cleanliness": ["clean", "dirty", "limpio", "sucio"],
        "service": ["staff", "service", "personal", "servicio"],
        "room": ["room", "habitación"],
        "food": ["food", "breakfast", "comida"],
        "noise": ["noise", "ruido"]
    }

    lower = text.lower()
    for aspect, words in keywords.items():
        if any(w in lower for w in words):
            aspects.append(aspect)

    return aspects
