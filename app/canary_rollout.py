# canary_rollout.py
baseline = {"error_rate": 0.01, "p95_latency_ms": 120}
canary = {"error_rate": 0.025, "p95_latency_ms": 350}

def check_canary(baseline, canary):
    if canary["error_rate"] > 1.5 * baseline["error_rate"]:
        return "rollback"
    if canary["p95_latency_ms"] > baseline["p95_latency_ms"] + 300:
        return "rollback"
    return "promote"

decision = check_canary(baseline, canary)
print(f"AI recommendation: {decision}")
