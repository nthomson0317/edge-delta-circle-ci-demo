import pytest
from app.calculator import slow_api_call

def test_api_flakiness():
    """Simulates a flaky dependency for demo purposes."""
    try:
        result = slow_api_call()
        assert result == "ok"
    except TimeoutError:
        pytest.fail("API call failed: timeout")
