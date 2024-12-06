from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL

class Utils:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def call(self, query: str):
        response = self.client.chat.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": query}]
        )
        return True, response.choices[0].message['content']

OpenaiMgr = Utils(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)