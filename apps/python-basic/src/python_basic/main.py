from fastapi import FastAPI
from python_basic.api.routes_chat import router as chat_router

app = FastAPI(title="AI Agent Service", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "OK"}


app.include_router(chat_router, prefix="/api")
