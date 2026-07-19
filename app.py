import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent_answer, get_cache_stats
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

app = FastAPI(
    title="AWS Docs RAG Chatbot",
    description="Local demo chatbot for AWS documentation using a Bedrock-backed retrieval flow.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] | None = None


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "aws-docs-chatbot"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Please provide a question.")

    return ChatResponse(response=agent_answer(message, history=request.history))


@app.get("/cache-stats")
def cache_stats() -> dict:
    return get_cache_stats()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
