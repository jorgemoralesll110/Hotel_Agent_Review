from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(review: str):

    prompt = f"""
You are a professional hotel customer service assistant.

You have access to external tools that provide:
- Review analysis (language, sentiment, aspects)
- Service guidelines for handling customer issues

Based on the information obtained from these tools, generate a polite,
empathetic and professional response. Follow service guidelines and
address the specific issues mentioned.

Customer review:
{review}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )

    return response.choices[0].message.content
