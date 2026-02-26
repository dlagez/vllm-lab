from fastapi.testclient import TestClient

from server.gateway import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


def test_chat_completion_local_fallback():
    payload = {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "messages": [{"role": "user", "content": "1+1 equals what?"}],
        "temperature": 0.0,
        "max_tokens": 10,
    }
    resp = client.post("/v1/chat/completions", json=payload)
    assert resp.status_code == 200
    text = resp.json()["choices"][0]["message"]["content"]
    assert "2" in text
