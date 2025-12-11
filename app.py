from openai import OpenAI
from tools.sentiment_analyzer.server import SentimentAnalyzer
from tools.response_generator.server import ResponseGenerator
from tools.review_manager.server import ReviewManager

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

sent_tool = SentimentAnalyzer()
resp_tool = ResponseGenerator()
rev_tool = ReviewManager()

def run_agent(user_review):

    # 1) Analizar sentimiento
    result = sent_tool.analyze_sentiment(user_review)
    sentiment = result["sentiment"]

    # 2) Generar respuesta automática
    auto_reply = resp_tool.generate_reply(user_review, sentiment)["reply"]

    # 3) Guardar reseña + respuesta
    rev_tool.save_review(user_review, auto_reply)

    # 4) Mejorar la respuesta con el LLM
    llm_output = client.chat.completions.create(
        model="llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": "Mejora el tono manteniendo la intención original."},
            {"role": "user", "content": auto_reply}
        ]
    )

    final_reply = llm_output.choices[0].message.content

    return final_reply