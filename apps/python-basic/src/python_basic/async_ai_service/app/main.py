from fastapi import FastAPI
import logging

# Ensure root logger is configured so module-level loggers are emitted
logging.basicConfig(level=logging.INFO)
from python_basic.async_ai_service.app.schemas import ChatRequest, ChatResponse
from python_basic.async_ai_service.app.services import LLMService

app = FastAPI(title="Async AI Service")
llm_service = LLMService()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    answer, elapsed_ms = await llm_service.chat(request.question)
    return ChatResponse(answer=answer, elapsed_ms=elapsed_ms)
