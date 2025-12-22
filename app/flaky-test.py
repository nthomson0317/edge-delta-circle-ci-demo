# app/flaky-test.py
import random
import sys
import time

time.sleep(random.uniform(0.5, 2.0))

if random.random() < 0.4:
    print("test_payment_timeout FAILED")
    sys.exit(1)
else:
    print("test_payment_timeout PASSED")
    sys.exit(0)
