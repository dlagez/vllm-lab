from config import load_client_config

import requests

config = load_client_config()

base_url = (config.get('OPENAI_BASE_URL') or '').rstrip('/')
model = config.get('MODEL_NAME') or ''
api_key = (config.get('OPENAI_API_KEY') or '').strip()

if not base_url or not model:
    raise RuntimeError('Missing OPENAI_BASE_URL or MODEL_NAME in .env')

url = f"{base_url}/chat/completions"
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
