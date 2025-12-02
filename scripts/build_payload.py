#!/usr/bin/env python3
# scripts/build_payload.py
import json
import os
import datetime
import sys
import re

REPORT_FILE = "pytest_output.txt"

def read_pytest_output(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def extract_failed_tests(pytext):
    # simple heuristic: lines that start with "FAILED " or contain "FAILED <path>::<testname>"
    failed = []
    for line in pytext.splitlines():
        line = line.strip()
        # pytest summary lines like: "FAILED tests/test_flaky.py::test_always_fails - AssertionError: ..."
        m = re.match(r"FAILED\s+(.+?)(?:\s|$)", line)
        if m:
            failed.append(m.group(1))
            continue
        # alternate "tests/test_x.py::test_name FAILED"
        if " FAILED " in line:
            parts = line.split()
            for p in parts:
                if p.endswith("::"):
                    continue
            # fallback: collect anything with :: in it
            tokens = [t for t in parts if "::" in t]
            failed.extend(tokens)
    return failed

def main():
    text = read_pytest_output(REPORT_FILE)
    status = "failed" if ("FAILED" in text or "ERROR" in text) else "passed"
    failed_tests = extract_failed_tests(text)

    payload = {
        "job": os.getenv("CIRCLE_JOB"),
        "repo": os.getenv("CIRCLE_PROJECT_REPONAME"),
        "branch": os.getenv("CIRCLE_BRANCH"),
        "commit": os.getenv("CIRCLE_SHA1"),
        "workflow": os.getenv("CIRCLE_WORKFLOW_ID"),
        "status": status,
        "failed_tests": failed_tests,
        "raw_logs": text,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    out = json.dumps(payload, indent=2)
    print("Generated build.json:")
    print(out)
    with open("build.json", "w", encoding="utf-8") as f:
        f.write(out)

if __name__ == "__main__":
    main()
