from fastapi import APIRouter, Depends
from typing import Annotated
from python_basic.schemas.chat import ChatRequest, ChatResponse
from python_basic.get_current_user import CurrentUser, get_current_user

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: Annotated[CurrentUser, Depends(get_current_user)],
) -> ChatResponse:
    return ChatResponse(
        answer=f"收到问题{user.tenant_id}/{user.user_id}：{request.question}",
        model="demo-model",
    )
