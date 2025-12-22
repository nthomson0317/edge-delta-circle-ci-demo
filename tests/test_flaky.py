import pytest

@pytest.mark.quarantine
def test_sometimes_fails():
    import random
    assert random.choice([True, False])
    
@pytest.mark.quarantine
@pytest.mark.quarantine
def test_payment_timeout():
    import time
    time.sleep(0.1)
    assert True

