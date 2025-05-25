import pytest
from session8 import multiply

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5
    assert multiply(0, 10) == 0
    assert multiply(-2, -3) == 6
    assert multiply(1.5, 2) == 3.0