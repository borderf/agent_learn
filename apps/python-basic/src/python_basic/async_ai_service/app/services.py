import asyncio
import logging
import time
import httpx
from python_basic.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    async def chat(self, question: str) -> tuple[str, float]:
        start = time.perf_counter()
        logger.info(
            "LLM config: base_url=%s, model=%s, key=%s",
            settings.openai_base_url,
            settings.default_model,
            settings.openai_api_key if settings.openai_api_key else "EMPTY",
        )
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    f"{settings.openai_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.default_model,
                        "messages": [
                            {"role": "user", "content": question},
                        ],
                        "temperature": 0.7,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                answer = data["choices"][0]["message"]["content"]
        except httpx.TimeoutException:
            elapsed = (time.perf_counter() - start) * 1000
            logger.error(
                "LLM call timed out after %.0f ms (question: %.50s)", elapsed, question
            )
            raise
        except httpx.HTTPStatusError as e:
            elapsed = (time.perf_counter() - start) * 1000
            logger.error(
                "LLM API error: %s (status=%s, question: %.50s)",
                e.response.text,
                e.response.status_code,
                question,
            )
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "LLM call took %.0f ms, tokens: %s", elapsed_ms, data.get("usage", {})
        )
        return answer, elapsed_ms
