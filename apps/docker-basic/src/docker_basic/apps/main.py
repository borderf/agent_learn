from fastapi import FastAPI

app = FastAPI(
    title="Docker Basic App",
    description="A simple FastAPI application running in Docker",
    version="1.0.0",
)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
