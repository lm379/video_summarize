from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
)

completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "你是谁？"},
    ],
)

print(completion.choices[0].message)