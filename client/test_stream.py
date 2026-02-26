import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

base_url = os.getenv('OPENAI_BASE_URL', 'http://127.0.0.1:8000/v1').rstrip('/')
url = f"{base_url}/chat/completions"
model = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-3B-Instruct')
api_key = os.getenv('OPENAI_API_KEY', '').strip()
headers = {'Authorization': f'Bearer {api_key}'} if api_key and api_key != 'EMPTY' else {}

payload = {
    'model': model,
    'messages': [{'role': 'user', 'content': 'Explain what vLLM is in one sentence.'}],
    'temperature': 0.2,
    'max_tokens': 64,
    'stream': True,
}

with requests.post(url, json=payload, headers=headers, stream=True, timeout=60) as resp:
    resp.raise_for_status()
    for line in resp.iter_lines(decode_unicode=True):
        if line:
            print(line)
