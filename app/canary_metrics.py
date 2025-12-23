#!/usr/bin/env python3
import requests
import random
import os
import json
from datetime import datetime

EDGE_DELTA_HTTP_URL = "https://6ebf4e82-073c-426b-9f56-f9b1915c6ab1-http-us-west2-cf.aws.edgedelta.com"
SERVICE_NAME = os.getenv("SERVICE_NAME", "http-80")
BRANCH = os.getenv("CIRCLE_BRANCH", "demo/canary")
REPO = os.getenv("CIRCLE_PROJECT_REPONAME", "edge-delta-circle-ci-demo")

def emit_request_log(variant: str):
    for i in range(5):
        latency = random.randint(100, 300)
        status = 200 if random.random() > 0.1 else 500
        log = {
            "type": "canary_probe.request",
            "service.name": SERVICE_NAME,
            "repo": REPO,
            "branch": BRANCH,
            "deployment.variant": variant,
            "response_time_ms": latency,
            "status_code": status,
            "success": status < 400,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        requests.post(EDGE_DELTA_HTTP_URL, json=log)

def emit_summary_log(variant: str, metrics: dict):
    summary = {
        "type": "canary_probe.summary",
        "service.name": SERVICE_NAME,
        "repo": REPO,
        "branch": BRANCH,
        "deployment.variant": variant,
        "error_rate": metrics["error_rate"],
        "p95_latency_ms": metrics["p95_latency_ms"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    requests.post(EDGE_DELTA_HTTP_URL, json=summary)

baseline = {
    "error_rate": 0.01,
    "p95_latency_ms": 120
}

canary = {
    "error_rate": 0.01 + random.random() * 0.02,
    "p95_latency_ms": 120 + random.randint(0, 100)
}

emit_request_log("baseline")
emit_summary_log("baseline", baseline)

emit_request_log("canary")
emit_summary_log("canary", canary)

print("Sent canary and baseline metrics to Edge Delta")
