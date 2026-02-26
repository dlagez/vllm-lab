from config import load_client_config

import requests

config = load_client_config()


def _build_url() -> str:
    base_url = (config.get('OPENAI_BASE_URL') or '').rstrip('/')
    if not base_url:
        raise RuntimeError('Missing OPENAI_BASE_URL in .env')
    return f"{base_url}/chat/completions"


def _build_headers() -> dict[str, str]:
    api_key = (config.get('OPENAI_API_KEY') or '').strip()
    if api_key and api_key != 'EMPTY':
        return {'Authorization': f'Bearer {api_key}'}
    return {}


def _model_name() -> str:
    model = config.get('MODEL_NAME') or ''
    if not model:
        raise RuntimeError('Missing MODEL_NAME in .env')
    return model


def test_chat_completion():
    payload = {
        'model': _model_name(),
        'messages': [{'role': 'user', 'content': '1+1 equals what?'}],
        'temperature': 0.0,
        'max_tokens': 10,
    }

    res = requests.post(_build_url(), json=payload, headers=_build_headers(), timeout=60)
    assert res.status_code == 200

    content = res.json()['choices'][0]['message']['content']
    assert '2' in content
