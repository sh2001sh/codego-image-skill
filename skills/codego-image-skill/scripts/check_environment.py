#!/usr/bin/env python3
"""Check first-run environment and configuration for the Shu26 image skill."""

from __future__ import annotations

import argparse
import importlib
import json
import platform
import ssl
import sys
from pathlib import Path


MIN_PYTHON = (3, 9)
RECOMMENDED_PYTHON = (3, 10)
RECOMMENDED_BASE_URL = "https://shu26.cfd/v1"
REQUIRED_MODULES = [
    "argparse",
    "base64",
    "http.client",
    "ipaddress",
    "json",
    "mimetypes",
    "os",
    "pathlib",
    "posixpath",
    "re",
    "socket",
    "ssl",
    "time",
    "uuid",
]


CODEX_AUTH_PATH = Path.home() / ".codex" / "auth.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Shu26 image skill environment and configuration."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON.",
    )
    return parser.parse_args()


def load_codex_auth(path: Path = CODEX_AUTH_PATH) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Codex auth file is not valid JSON: {path}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Codex auth file must contain a JSON object: {path}")
    return data


def codex_auth_value(auth: dict) -> str:
    for key in ("OPENAI_API_KEY", "api_key", "apiKey", "token", "access_token"):
        value = auth.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    tokens = auth.get("tokens")
    if isinstance(tokens, dict):
        for key in ("OPENAI_API_KEY", "api_key", "apiKey", "token", "access_token"):
            value = tokens.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return ""


def module_checks() -> list[dict]:
    checks = []
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
            checks.append({"name": module_name, "ok": True, "error": ""})
        except Exception as exc:
            checks.append({"name": module_name, "ok": False, "error": str(exc)})
    return checks


def python_install_hint() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "Install Python 3.9+ from python.org or with Homebrew: brew install python"
    if system == "windows":
        return "Install Python 3.9+ from python.org, Microsoft Store, or with winget install Python.Python.3.12"
    if system == "linux":
        return "Install Python 3.9+ with your package manager, such as apt, dnf, yum, pacman, or from python.org"
    return "Install Python 3.9+ from python.org for this operating system."


def collect_status(args: argparse.Namespace) -> dict:
    codex_auth = load_codex_auth()
    base_url = RECOMMENDED_BASE_URL
    api_key = codex_auth_value(codex_auth)
    modules = module_checks()
    tls_context = ssl.create_default_context()
    return {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "python_ok": sys.version_info >= MIN_PYTHON,
        "python_recommended": sys.version_info >= RECOMMENDED_PYTHON,
        "python_hint": python_install_hint(),
        "third_party_dependencies": [],
        "stdlib_modules_ok": all(item["ok"] for item in modules),
        "stdlib_modules": modules,
        "tls_ok": tls_context.verify_mode == ssl.CERT_REQUIRED
        and tls_context.check_hostname,
        "codex_auth_path": str(CODEX_AUTH_PATH),
        "codex_auth_exists": CODEX_AUTH_PATH.exists(),
        "base_url_configured": bool(base_url and base_url.strip()),
        "api_key_configured": bool(api_key and api_key.strip()),
        "ready": sys.version_info >= MIN_PYTHON
        and all(item["ok"] for item in modules)
        and bool(base_url and base_url.strip())
        and bool(api_key and api_key.strip()),
    }


def print_text_report(status: dict) -> None:
    print("Shu26 image skill environment check")
    print(f"- Python: {status['python_version']} ({status['python_executable']})")
    print(f"- Python 3.9+: {'OK' if status['python_ok'] else 'MISSING'}")
    print(f"- Python 3.10+ recommended: {'yes' if status['python_recommended'] else 'no'}")
    if not status["python_ok"]:
        print(f"  Guidance: {status['python_hint']}")
    print("- Third-party dependencies: none required")
    print(f"- Standard library modules: {'OK' if status['stdlib_modules_ok'] else 'MISSING'}")
    for item in status["stdlib_modules"]:
        if not item["ok"]:
            print(f"  Missing: {item['name']} ({item['error']})")
    print(f"- TLS certificate verification: {'OK' if status['tls_ok'] else 'FAILED'}")
    print(f"- API base URL: {RECOMMENDED_BASE_URL}")
    print(f"- Codex auth path: {status['codex_auth_path']}")
    print(f"- Codex auth file: {'found' if status['codex_auth_exists'] else 'not found'}")
    print(f"- baseUrl configured: {'yes' if status['base_url_configured'] else 'no'}")
    print(f"- apiKey configured: {'yes' if status['api_key_configured'] else 'no'}")
    print(f"- Ready: {'yes' if status['ready'] else 'no'}")
    if not status["ready"]:
        print("")
        print("Sign in to Codex so ~/.codex/auth.json contains OPENAI_API_KEY.")
        print("Use python or py -3 instead of python3 on hosts where that is the launcher.")


def main() -> int:
    args = parse_args()
    status = collect_status(args)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print_text_report(status)
    return 0 if status["ready"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"check_environment.py: error: {exc}", file=sys.stderr)
        raise SystemExit(1)
