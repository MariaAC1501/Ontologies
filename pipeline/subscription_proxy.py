"""Connect stock OntoCast to the local Pi Codex subscription proxy."""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PROXY_API_KEY = "subscription-proxy"  # Non-secret SDK placeholder, not an OpenAI key.
DEFAULT_BASE_URL = "http://127.0.0.1:8977/v1"
REPO_ROOT = Path(__file__).resolve().parents[1]


class SubscriptionProxyError(RuntimeError):
    """The subscription proxy is misconfigured or unavailable."""


def subscription_proxy_base() -> str:
    if os.environ.get("LLM_BASE_URL"):
        return os.environ["LLM_BASE_URL"]
    env_file = REPO_ROOT / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.strip().partition("=")
            if separator and key.strip() == "LLM_BASE_URL":
                return value.strip().strip('"').strip("'") or DEFAULT_BASE_URL
    return DEFAULT_BASE_URL


def validate_subscription_settings(base_url: str) -> None:
    """Reject real keys and non-local endpoints before sending any request."""
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY") not in (
        None, "", PROXY_API_KEY
    ):
        raise SubscriptionProxyError(
            "Direct OpenAI API keys are disabled. Use the Pi Codex subscription "
            "proxy; LLM_API_KEY may only be the non-secret 'subscription-proxy' placeholder."
        )
    try:
        url = urllib.parse.urlsplit(base_url)
        loopback = url.hostname == "localhost" or ipaddress.ip_address(
            url.hostname or ""
        ).is_loopback
        valid = (
            url.scheme == "http" and loopback and not url.username and not url.password
            and not url.query and not url.fragment and url.path.rstrip("/") == "/v1"
        )
        # Accessing port also validates its syntax and range.
        _ = url.port
    except ValueError:
        valid = False
    if not valid:
        raise SubscriptionProxyError(
            "LLM_BASE_URL must point to the local Pi Codex proxy, "
            "for example http://127.0.0.1:8977/v1."
        )


def require_subscription_proxy(base_url: str) -> None:
    validate_subscription_settings(base_url)
    health = base_url.rstrip("/").removesuffix("/v1") + "/health"
    try:
        with urllib.request.urlopen(health, timeout=5) as response:
            payload = json.load(response)
        if not isinstance(payload, dict) or payload.get("provider") != "openai-codex":
            raise SubscriptionProxyError(
                "The local endpoint is not the Pi Codex subscription proxy."
            )
    except (OSError, urllib.error.URLError, ValueError) as error:
        raise SubscriptionProxyError(
            f"Subscription proxy is not reachable at {health}. "
            "Start pipeline/tools/pi_codex_openai_proxy.mjs."
        ) from error


def subscription_environment(base_url: str) -> dict[str, str]:
    """Pin routing and the dummy key even when shell variables override dotenv files."""
    validate_subscription_settings(base_url)
    return {
        **os.environ,
        "LLM_PROVIDER": "openai",
        "LLM_BASE_URL": base_url,
        "LLM_API_KEY": PROXY_API_KEY,
        "ONTOLOGY_CRITIC_PASSES": "0",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=subscription_proxy_base())
    args = parser.parse_args()
    try:
        require_subscription_proxy(args.base_url)
    except SubscriptionProxyError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
