import requests

url = "http://localhost:8000/v1/chat/completions"

payload = {
    "model": "Qwen/Qwen2.5-3B-Instruct",
    "messages": [{"role": "user", "content": "Explain what vLLM is in one sentence."}],
    "temperature": 0.2,
    "max_tokens": 64,
    "stream": True,
}

with requests.post(url, json=payload, stream=True, timeout=60) as resp:
    resp.raise_for_status()
    for line in resp.iter_lines(decode_unicode=True):
        if line:
            print(line)
