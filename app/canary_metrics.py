# canary_metrics.py
import requests
import random
import os
from datetime import datetime
import json
import requests

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
# Emit simulated canary HTTP request logs with latency + status
logs = [
    {
        "message": "request completed",
        "service.name": "http-80",
        "ed.tag": "nicholas_demo",
        "http.status_code": random.choice([200, 200, 200, 500]),
        "duration_ms": random.randint(80, 450),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    for _ in range(50)
]

for log in logs:
    requests.post(
        EDGE_DELTA_HTTP_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(log)
    )

response = requests.post(EDGE_DELTA_HTTP_URL, json=payload)
print("Sent metrics to Edge Delta:", response.status_code)
