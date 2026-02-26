from pathlib import Path

from dotenv import dotenv_values


def load_client_config() -> dict[str, str]:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    raw = dotenv_values(env_path)
    normalized: dict[str, str] = {}
    for k, v in raw.items():
        if k is None:
            continue
        key = k.replace("\ufeff", "").strip()
        normalized[key] = (v or "").strip()
    return normalized
