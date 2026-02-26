import requests

url = "http://localhost:8000/v1/chat/completions"

payload = {
    "model": "Qwen/Qwen2.5-3B-Instruct",
    "messages": [
        {"role": "user", "content": "解释什么是 vLLM"}
    ],
    "temperature": 0.2,
    "max_tokens": 128
}

res = requests.post(url, json=payload)
print(res.json()["choices"][0]["message"]["content"])