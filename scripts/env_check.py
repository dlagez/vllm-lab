import importlib
import os
import platform
import sys

DEPS = [
    "fastapi",
    "uvicorn",
    "yaml",
    "httpx",
    "requests",
]


def check_import(name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(name)
        version = getattr(module, "__version__", "unknown")
        return True, str(version)
    except Exception as exc:  # pragma: no cover
        return False, str(exc)


def main() -> int:
    print("== Environment Check ==")
    print(f"Python   : {sys.version.split()[0]}")
    print(f"Platform : {platform.platform()}")
    print(f"CWD      : {os.getcwd()}")
    print("")

    failed = False
    for dep in DEPS:
        ok, detail = check_import(dep)
        if ok:
            print(f"[OK]   {dep:<10} {detail}")
        else:
            failed = True
            print(f"[FAIL] {dep:<10} {detail}")

    try:
        import vllm  # type: ignore

        print(f"[OK]   {'vllm':<10} {vllm.__version__}")
    except Exception as exc:
        print(f"[WARN] {'vllm':<10} {exc}")
        print("       Gateway can still run in local_fallback mode.")

    print("")
    print("Environment variables:")
    for key in ["OPENAI_BASE_URL", "OPENAI_API_KEY", "MODEL_NAME", "VLLM_BASE_URL", "VLLM_API_KEY"]:
        print(f"- {key}={os.getenv(key, '')}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
