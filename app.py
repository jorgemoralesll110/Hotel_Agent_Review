from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(review: str):

    result = subprocess.run(
        ["fastmcp", "call", "hotel-review-processor.analyze_review", review],
        capture_output=True,
        text=True
    )

    analysis = result.stdout

    prompt = f"""
You are a professional hotel customer service assistant.

The following analysis has been obtained from an external tool:
{analysis}

Using this information, respond politely, empathetically and specifically.
Avoid generic responses.

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
