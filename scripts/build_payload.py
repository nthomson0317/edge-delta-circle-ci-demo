import json, os, subprocess, time, platform, re

def run_pytest_and_capture():
    """
    Runs pytest and returns:
      - raw output
      - duration (seconds)
    """
    start = time.time()
    result = subprocess.run(
        ["pytest", "-q", "--disable-warnings", "--maxfail=1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    duration = time.time() - start
    return result.stdout, duration


def parse_pytest_output(text):
    """
    Extracts structured metadata from pytest output.
    Handles FAILED, ERROR, passed, etc.
    """
    failed_tests = []
    errors = []
    passed = 0
    failed = 0
    errored = 0

    # Match lines like:
    #   FAILED tests/test_calculator.py::test_divide_zero
    #   ERROR tests/test_foo.py::test_bar
    fail_pattern = r"(FAILED|ERROR)\s+([^\s]+)"
    for match in re.finditer(fail_pattern, text):
        status, testname = match.groups()
        if status == "FAILED":
            failed_tests.append(testname)
            failed += 1
        else:
            errors.append(testname)
            errored += 1

    # Count passed tests
    pass_pattern = r"(\d+)\s+passed"
    pass_match = re.search(pass_pattern, text)
    if pass_match:
        passed = int(pass_match.group(1))

    # Determine overall status
    status = "failed" if (failed > 0 or errored > 0) else "passed"

    return {
        "status": status,
        "passed": passed,
        "failed": failed,
        "errors": errored,
        "failed_tests": failed_tests,
        "error_tests": errors,
    }


def build_payload(pytest_raw, duration):
    """Create the full JSON payload for Edge Delta."""
    metadata = parse_pytest_output(pytest_raw)

    payload = {
        "job": os.environ.get("CIRCLE_JOB", ""),
        "repo": os.environ.get("CIRCLE_PROJECT_REPONAME", ""),
        "repo_url": os.environ.get("CIRCLE_REPOSITORY_URL", ""),
        "branch": os.environ.get("CIRCLE_BRANCH", ""),
        "commit": os.environ.get("CIRCLE_SHA1", ""),
        "workflow_id": os.environ.get("CIRCLE_WORKFLOW_ID", ""),
        "workflow_url": f"{os.environ.get('CIRCLE_BUILD_URL', '')}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),

        # Execution details
        "duration_seconds": round(duration, 3),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),

        # Pytest summary
        "status": metadata["status"],
        "passed": metadata["passed"],
        "failed": metadata["failed"],
        "errors": metadata["errors"],
        "failed_tests": metadata["failed_tests"],
        "error_tests": metadata["error_tests"],

        # Raw logs included for AI teammate + debugging
        "raw_logs": pytest_raw,
    }

    return payload


if __name__ == "__main__":
    print("Running pytest...")
    pytest_output, duration = run_pytest_and_capture()

    print("Saving pytest output to pytest_output.txt")
    with open("pytest_output.txt", "w") as f:
        f.write(pytest_output)

    payload = build_payload(pytest_output, duration)

    with open("build.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("\nGenerated richer build.json:")
    print(json.dumps(payload, indent=2))
