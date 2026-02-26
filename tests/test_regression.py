from fastapi.testclient import TestClient

from server.gateway import app

client = TestClient(app)


def test_empty_messages_returns_400():
    payload = {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "messages": [],
    }
    resp = client.post("/v1/chat/completions", json=payload)
    assert resp.status_code == 400
