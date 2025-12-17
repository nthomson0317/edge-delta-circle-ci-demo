import os

def test_intentional_ci_failure():
    # Fail only in CI on pull requests
    if os.getenv("CIRCLE_PULL_REQUEST"):
        assert False, "Intentional CI failure for AI Teammate demo"
