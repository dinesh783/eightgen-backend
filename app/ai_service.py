import os
from dotenv import load_dotenv

load_dotenv()

USE_OPENAI = False  # change to True later

def get_ai_response(prompt: str) -> str:
    if not USE_OPENAI:
        return f"[Mock AI] You said: {prompt}"

    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content