#!/usr/bin/env python3
import json
import os
import sys
import time
from typing import Dict, Optional

try:
    import requests
except ImportError:
    print("ERROR: requests is not installed. Ensure requirements.txt is installed.")
    sys.exit(2)


def getenv(name: str, default: Optional[str] = None) -> Optional[str]:
    val = os.getenv(name)
    return val if val is not None and val != "" else default


def to_int(name: str, default: int) -> int:
    try:
        return int(getenv(name, str(default)))
    except Exception:
        return default


def load_headers() -> Dict[str, str]:
    raw = getenv("ED_CANARY_HEADERS")
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
        print("WARN: ED_CANARY_HEADERS is not a JSON object. Ignoring.")
        return {}
    except Exception as e:
        print(f"WARN: Failed to parse ED_CANARY_HEADERS as JSON: {e}")
        return {}


def main() -> int:
    url = getenv("ED_CANARY_URL")
    if not url:
        print("ERROR: ED_CANARY_URL is required.")
        return 2

    method = (getenv("ED_CANARY_METHOD", "GET") or "GET").upper()
    timeout = float(getenv("ED_CANARY_TIMEOUT", "10"))
    expected_status = to_int("ED_CANARY_EXPECTED_STATUS", 200)
    search_text = getenv("ED_CANARY_SEARCH_TEXT")
    retries = to_int("ED_CANARY_RETRIES", 2)
    backoff = float(getenv("ED_CANARY_RETRY_BACKOFF", "2"))

    headers = load_headers()
    body = getenv("ED_CANARY_BODY")
    json_flag = getenv("ED_CANARY_JSON", "false").lower() in {"1", "true", "yes"}

    session = requests.Session()

    attempt = 0
    while True:
        attempt += 1
        try:
            print(f"Canary attempt {attempt}: {method} {url}")
            kwargs = {"timeout": timeout, "headers": headers}
            if method in {"POST", "PUT", "PATCH"} and body is not None:
                if json_flag:
                    kwargs["json"] = json.loads(body) if body else None
                else:
                    kwargs["data"] = body

            resp = session.request(method, url, **kwargs)
            status = resp.status_code
            print(f"Status: {status}")

            if status != expected_status:
                raise AssertionError(f"Expected status {expected_status} but got {status}")

            if search_text is not None:
                if search_text not in resp.text:
                    raise AssertionError("Expected text not found in response body")
                print("Search text found in response body")

            print("Canary probe succeeded")
            return 0
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt > retries:
                print("Canary probe failed after retries")
                return 1
            time.sleep(backoff)


if __name__ == "__main__":
    sys.exit(main())
