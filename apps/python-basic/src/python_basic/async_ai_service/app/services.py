import asyncio
import logging
import time
import httpx
import tenacity
from typing import AsyncGenerator
import json
from python_basic.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        self._client: httpx.AsyncClient | None = None
        # 控制最大并发数量
        self._semaphore = asyncio.Semaphore(10)

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            timeout = httpx.Timeout(connect=5.0, read=60.0, write=5.0, pool=5.0)
            limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
            self._client = httpx.AsyncClient(timeout=timeout, limits=limits)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
        retry=tenacity.retry_if_exception_type(
            (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError)
        ),
        retry_error_callback=lambda retry_state: (
            retry_state.outcome.result()
            if isinstance(retry_state.outcome.exception(), httpx.HTTPStatusError)
            and retry_state.outcome.exception().response.status_code < 500
            and retry_state.outcome.exception().response.status_code != 429
            else None
        ),
    )
    async def chat(self, question: str) -> tuple[str, float]:
        async with self._semaphore:
            start = time.perf_counter()
            client = await self._get_client()
            try:
                resp = await client.post(
                    f"{settings.openai_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.default_model,
                        "messages": [{"role": "user", "content": question}],
                        "temperature": 0.7,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                answer = data["choices"][0]["message"]["content"]
            except httpx.TimeoutException:
                elapsed = (time.perf_counter() - start) * 1000
                logger.error(
                    "LLM call timed out (%.0f ms), question: %.50s", elapsed, question
                )
                raise
            except httpx.HTTPStatusError as e:
                elapsed = (time.perf_counter() - start) * 1000
                logger.error(
                    "LLM API error %s: %s",
                    e.response.status_code,
                    e.response.text[:200],
                )
                raise
            except httpx.RequestError as e:
                elapsed = (time.perf_counter() - start) * 1000
                logger.error("LLM network error: %s", e)
                raise
            except (KeyError, json.JSONDecodeError) as e:
                elapsed = (time.perf_counter() - start) * 1000
                logger.error("LLM response parse error: %s", e)
                raise
            except asyncio.CancelledError:
                # 任务取消，不必记录错误，直接传播
                raise

            elapsed_ms = (time.perf_counter() - start) * 1000
            usage = data.get("usage", {})
            logger.info("LLM call took %.0f ms, tokens: %s", elapsed_ms, usage)
            return answer, elapsed_ms

    async def chat_stream(self, question: str) -> AsyncGenerator[str, None]:
        """
        流式对话，每产出新的 token 立即 yield。
        使用方式：
            async for token in service.chat_stream("hello"):
                print(token, end="", flush=True)
        """
        async with self._semaphore:
            client = await self._get_client()
            try:
                async with client.stream(
                    "POST",
                    f"{settings.openai_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.default_model,
                        "messages": [{"role": "user", "content": question}],
                        "temperature": 0.7,
                        "stream": True,
                    },
                ) as resp:
                    resp.raise_for_status()
                    answer = ""
                    async for line in resp.aiter_lines():
                        if not line:  # 跳过空行
                            continue
                        line = line.strip()
                        if line.startswith("data:"):
                            content = line[5:].strip()  # 移除 "data:" 前缀
                            if content == "[DONE]":
                                break
                            try:
                                data = json.loads(content)
                                delta = data["choices"][0]["delta"]
                                content_token = delta.get("content")
                                if content_token is not None:
                                    answer += content_token
                                    yield content_token
                            except json.JSONDecodeError:
                                logger.warning(
                                    "Failed to parse stream chunk: %s", content
                                )
            except httpx.TimeoutException:
                logger.error("LLM stream timed out, question: %.50s", question)
                raise
            except httpx.HTTPStatusError as e:
                logger.error(
                    "LLM stream API error %s: %s",
                    e.response.status_code,
                    e.response.text[:200],
                )
                raise
            except httpx.RequestError as e:
                logger.error("LLM stream network error: %s", e)
                raise
