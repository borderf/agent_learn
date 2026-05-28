from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    model: str


# Field约束
class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=50)
    top_k: int = Field(default=8, ge=1, le=30)
    knowledge_base_id: str


# 嵌套模型
class SourceRef(BaseModel):
    doc_id: str
    title: str
    page: int | None = None
    score: float


class RagAnswer(BaseModel):
    answer: str
    sources: list[SourceRef] = Field(default_factory=list)
