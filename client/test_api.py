import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')


def _build_url() -> str:
    base_url = os.getenv('OPENAI_BASE_URL', 'http://127.0.0.1:8000/v1').rstrip('/')
    return f"{base_url}/chat/completions"


def _build_headers() -> dict[str, str]:
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if api_key and api_key != 'EMPTY':
        return {'Authorization': f'Bearer {api_key}'}
    return {}


def test_chat_completion():
    payload = {
        'model': os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-3B-Instruct'),
        'messages': [{'role': 'user', 'content': '1+1 equals what?'}],
        'temperature': 0.0,
        'max_tokens': 10,
    }

    res = requests.post(_build_url(), json=payload, headers=_build_headers(), timeout=60)
    assert res.status_code == 200

    content = res.json()['choices'][0]['message']['content']
    assert '2' in content
