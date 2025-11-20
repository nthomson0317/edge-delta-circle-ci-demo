# app/calculator.py

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def slow_api_call():
    # Simulate a flaky API or network dependency
    import random
    if random.random() < 0.3:
        raise TimeoutError("API timed out")
    return "ok"
