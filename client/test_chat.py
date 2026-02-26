from pathlib import Path

import requests
from dotenv import dotenv_values

env_path = Path(__file__).resolve().parents[1] / '.env'
config = dotenv_values(env_path)

base_url = (config.get('OPENAI_BASE_URL') or '').rstrip('/')
model = config.get('MODEL_NAME') or ''
api_key = (config.get('OPENAI_API_KEY') or '').strip()

if not base_url or not model:
    raise RuntimeError('Missing OPENAI_BASE_URL or MODEL_NAME in .env')

url = f"{base_url}/chat/completions"
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
