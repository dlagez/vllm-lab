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
    'messages': [{'role': 'user', 'content': 'Explain what vLLM is.'}],
    'temperature': 0.2,
    'max_tokens': 128,
}

res = requests.post(url, json=payload, headers=headers, timeout=60)
res.raise_for_status()
print(res.json()['choices'][0]['message']['content'])
