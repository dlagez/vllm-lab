import requests


def test_chat_completion():
    url = "http://localhost:8000/v1/chat/completions"

    payload = {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "messages": [{"role": "user", "content": "1+1 equals what?"}],
        "temperature": 0.0,
        "max_tokens": 10,
    }

    res = requests.post(url, json=payload, timeout=60)
    assert res.status_code == 200

    content = res.json()["choices"][0]["message"]["content"]
    assert "2" in content
