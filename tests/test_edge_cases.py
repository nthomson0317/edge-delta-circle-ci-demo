from app.calculator import add

def test_large_numbers():
    assert add(10**10, 10**10) == 2 * 10**10

def test_string_inputs_fail():
    try:
        add("a", 1)
    except TypeError:
        return
    assert False, "Expected TypeError for string inputs"
