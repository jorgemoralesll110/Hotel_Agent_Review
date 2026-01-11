from openai import OpenAI
from dotenv import load_dotenv
import os

from tools.language import detect_language
from tools.sentiment import analyze_sentiment
from tools.aspects import extract_aspects

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(review: str):

    language = detect_language(review)
    sentiment = analyze_sentiment(review)
    aspects = extract_aspects(review)

    system_prompt = f"""
You are a professional hotel customer service assistant.

Respond to the customer's review in a personalized, polite and empathetic way.
The response must NOT be generic.

Context:
- Language: {language}
- Sentiment: {sentiment}
- Mentioned aspects: {", ".join(aspects) if aspects else "none"}

Guidelines:
- Respond in the detected language.
- If the review is negative, acknowledge the problem and show willingness to improve.
- If the review is positive, thank the customer sincerely.
- Address specific aspects mentioned in the review.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": review}
        ]
    )

    return response.choices[0].message.content
