import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# Manages integration with the OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL")

# Management of errors related to Openrouter
class OpenRouterError(Exception):
    pass

# Function to send a message to the AI and return a response
async def chat_completion(messages: list[dict]) -> str:
    if not OPENROUTER_API_KEY:
        raise OpenRouterError("il manque la clé API OpenRouter")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_SITE_URL,
        "X-Title": OPENROUTER_APP_NAME,
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }

    # Asynchronous HTTP client
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise OpenRouterError(response.text)

        data = response.json()
        return data["choices"][0]["message"]["content"]
