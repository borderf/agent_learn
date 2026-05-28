from fastapi import APIRouter
from python_basic.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        answer=f"收到问题：{request.question}",
        model="demo-model",
    )
