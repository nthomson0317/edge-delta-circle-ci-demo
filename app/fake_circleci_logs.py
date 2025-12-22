# fake_circleci_logs.py
import json, time, random
from datetime import datetime
import requests

ENDPOINT = "http://caaecd16-2026-460e-8501-9e6563a1b2cf-http-us-west2-cf.aws.edgedelta.com"

def ts():
    return datetime.utcnow().isoformat() + "Z"

steps = [
    "Starting job 'build'",
    "Cloning repository...",
    "Using Python version 3.10",
    "Installing dependencies...",
    "Running tests...",
    "Test suite started",
]

fail_msgs = [
    "E AssertionError: expected status 200 but got 500",
    "E TimeoutError: operation timed out after 30s",
    "E ValueError: invalid configuration file",
]

# Simulate 20 CircleCI-style log lines
for i in range(20):
    line = random.choice(steps)
    if random.random() < 0.2:
        line = random.choice(fail_msgs)

    payload = {
        "timestamp": ts(),
        "job": "build",
        "executor": "docker",
        "line": line,
        "sequence": i,
        "level": "error" if line in fail_msgs else "info"
    }

    print("Sending:", payload)
    requests.post(ENDPOINT, json=payload)
    time.sleep(0.3)
