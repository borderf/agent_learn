from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import logging

# Ensure root logger is configured so module-level loggers are emitted
logging.basicConfig(level=logging.INFO)
from python_basic.async_ai_service.app.schemas import ChatRequest, ChatResponse
from python_basic.async_ai_service.app.services import LLMService

logger = logging.getLogger(__name__)

app = FastAPI(title="Async AI Service")
llm_service = LLMService()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    answer, elapsed_ms = await llm_service.chat(request.question)
    return ChatResponse(answer=answer, elapsed_ms=elapsed_ms)


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, http_request: Request):
    """
    流式问答接口，以 Server-Sent Events (SSE) 格式返回 token。
    """

    async def generate():
        try:
            async for token in llm_service.chat_stream(request.question):
                # 客户端断开时尽早退出
                if await http_request.is_disconnected():
                    logger.info("Client disconnected from /chat/stream")
                    break
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"
        except Exception:
            logger.exception("Error in chat_stream")
            yield "data: [ERROR] Internal server error\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲（如果部署在 Nginx 后）
        },
    )


async def main():
    service = LLMService()
    async for token in service.chat_stream("请介绍一下你自己"):
        print(token, end="", flush=True)
    print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
