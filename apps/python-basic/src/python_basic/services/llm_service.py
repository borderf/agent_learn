import httpx
from pydantic import BaseModel
from python_basic.core.config import settings


class LLMMessage(BaseModel):
    role: str
    content: str


class LLMService:
    async def chat(self, messages: list[LLMMessage]) -> str:
        payload: {
            "model": settings.default_model,
            "messages": [message.model_dump() for message in messages],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {settings.openai_api_key}"}

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{settings.openai_base_url.rstrip('/')}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


def get_llm_service() -> LLMService:
    return LLMService()
