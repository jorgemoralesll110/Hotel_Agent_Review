from openai import OpenAI
import os

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


def run_agent(user_review):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instruct",
        messages=[
            {"role": "system",
             "content": "Eres un agente que responde reseñas de hoteles de forma amable, formal y profesional."},
            {"role": "user", "content": user_review}
        ]
    )

    # LM Studio devuelve un objeto con .choices
    reply_text = response.choices[0].message.content

    # Devolvemos un string para Streamlit
    return reply_text