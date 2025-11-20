from app.calculator import add, divide

def test_add_basic():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_divide_basic():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    import pytest
    with pytest.raises(ValueError):
        divide(1, 0)
