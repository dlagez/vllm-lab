import json
import os
import time
import uuid
from typing import Any, AsyncGenerator

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="vLLM Gateway", version="0.1.0")

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "0.0.0.0")
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "8000"))
DEFAULT_MODEL = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-3B-Instruct")
VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "").rstrip("/")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "EMPTY")


class ChatCompletionRequest(BaseModel):
    model: str = Field(default=DEFAULT_MODEL)
    messages: list[dict[str, Any]]
    temperature: float | None = 0.7
    max_tokens: int | None = 128
    stream: bool | None = False


def _local_generate(messages: list[dict[str, Any]]) -> str:
    user_text = ""
    for message in reversed(messages):
        if message.get("role") == "user":
            user_text = str(message.get("content", "")).strip()
            break

    text = user_text.lower()
    if "1+1" in text or "1 + 1" in text:
        return "1 + 1 = 2."
    if "vllm" in text:
        return "vLLM is a high-throughput and memory-efficient LLM serving engine."
    if user_text:
        return f"Local fallback reply: {user_text}"
    return "Local fallback reply: empty prompt."


def _build_completion(model: str, content: str) -> dict[str, Any]:
    now = int(time.time())
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
        "object": "chat.completion",
        "created": now,
        "model": model or DEFAULT_MODEL,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }


async def _proxy_non_stream(req: ChatCompletionRequest) -> JSONResponse:
    url = f"{VLLM_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {VLLM_API_KEY}"}
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=req.model_dump(), headers=headers)
    return JSONResponse(content=resp.json(), status_code=resp.status_code)


async def _proxy_stream(req: ChatCompletionRequest) -> StreamingResponse:
    url = f"{VLLM_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {VLLM_API_KEY}"}
    payload = req.model_dump()
    payload["stream"] = True

    async def generator() -> AsyncGenerator[bytes, None]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as resp:
                if resp.status_code >= 400:
                    body = await resp.aread()
                    raise HTTPException(status_code=resp.status_code, detail=body.decode("utf-8"))
                async for line in resp.aiter_lines():
                    if line:
                        yield (line + "\n").encode("utf-8")

    return StreamingResponse(generator(), media_type="text/event-stream")


async def _local_stream(model: str, messages: list[dict[str, Any]]) -> StreamingResponse:
    content = _local_generate(messages)
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    now = int(time.time())

    async def generator() -> AsyncGenerator[bytes, None]:
        for token in content.split():
            chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": now,
                "model": model or DEFAULT_MODEL,
                "choices": [{"index": 0, "delta": {"content": token + " "}, "finish_reason": None}],
            }
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n".encode("utf-8")
        done_chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": now,
            "model": model or DEFAULT_MODEL,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(done_chunk, ensure_ascii=False)}\n\n".encode("utf-8")
        yield b"data: [DONE]\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "vLLM Gateway is running"}


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "mode": "proxy" if VLLM_BASE_URL else "local_fallback",
        "vllm_base_url": VLLM_BASE_URL or None,
        "model": DEFAULT_MODEL,
    }


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")

    if VLLM_BASE_URL:
        if req.stream:
            return await _proxy_stream(req)
        return await _proxy_non_stream(req)

    if req.stream:
        return await _local_stream(req.model, req.messages)

    content = _local_generate(req.messages)
    return _build_completion(req.model, content)


if __name__ == "__main__":
    uvicorn.run(app, host=GATEWAY_HOST, port=GATEWAY_PORT, reload=False)
