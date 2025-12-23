import requests
import time
import random
import os
import json

EDGE_DELTA_HTTP_URL = os.environ.get("https://6ebf4e82-073c-426b-9f56-f9b1915c6ab1-http-us-west2-cf.aws.edgedelta.com")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "http-80")

def send_request(status_code):
    log = {
        "service": SERVICE_NAME,
        "status_code": status_code,
        "response_time_ms": random.randint(100, 300),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    requests.post(EDGE_DELTA_HTTP_URL, json=log)
    print(f"Sent log: {log}")

# Simulate 20 requests: 12x 5xx, 8x 200
for _ in range(12):
    send_request(500)
for _ in range(8):
    send_request(200)
