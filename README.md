# vLLM Lab

A minimal lab project for running and testing a vLLM gateway setup.

## Prerequisites

- Python 3.10-3.12 (3.10 or 3.11 recommended)
- Latest `pip`
- NVIDIA GPU + CUDA (required for real vLLM inference)
- Git (optional)

Notes:
- `vllm` works best on Linux/WSL2.
- If installation fails on native Windows, use WSL2 Ubuntu.

## Create Environment

### Linux / macOS / WSL

```bash
cd /path/to/vllm-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configure .env

Use `.env` in the project root (ignored by git).

Example:

```env
OPENAI_BASE_URL=http://127.0.0.1:8000/v1
OPENAI_API_KEY=EMPTY
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
```

## Verify Installation

```powershell
python -V
pip -V
python -c "import fastapi, uvicorn, yaml, httpx; print('basic deps ok')"
python -c "import vllm; print(vllm.__version__)"
```

## Common Commands (placeholders)

```powershell
python server/gateway.py
pytest -q
python perf/load_test.py
```
