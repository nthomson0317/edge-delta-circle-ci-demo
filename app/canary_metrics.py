# canary_metrics.py
import requests
import random
import os
from datetime import datetime
import json

EDGE_DELTA_HTTP_URL = os.environ.get("EDGE_DELTA_HTTP_URL")

# Simulated baseline metrics
baseline = {
    "error_rate": 0.01,
    "p95_latency_ms": 120
}

# Simulated canary metrics
canary = {
    "error_rate": 0.01 + random.random() * 0.02,  # 1–3%
    "p95_latency_ms": 120 + random.randint(0, 100)
}

payload = {
    "repo": "edge-delta-circle-ci-demo",
    "branch": "demo/ai-ci-triage",
    "canary_metrics": canary,
    "baseline_metrics": baseline,
    "tags": {
        "service.name": "http-80",
        "ed.tag": "nicholas_demo"
    },
    "timestamp": datetime.utcnow().isoformat() + "Z"
}

logs = [
    {"pod": "canary-1", "msg": "request succeeded", "timestamp": datetime.utcnow().isoformat()},
    {"pod": "canary-2", "msg": "request failed", "timestamp": datetime.utcnow().isoformat()},
]

for log in logs:
    # Include the same tags for logs if desired
    log["tags"] = {"service.name": "http-80", "ed.tag": "nicholas_demo"}
    requests.post(EDGE_DELTA_HTTP_URL, headers={"Content-Type": "application/json"}, data=json.dumps(log))

response = requests.post(EDGE_DELTA_HTTP_URL, json=payload)
print("Sent metrics to Edge Delta:", response.status_code)
