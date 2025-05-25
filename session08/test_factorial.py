import pytest
from factorial import factorial

@pytest.mark.parametrize("input_value, expected_output", [
    (0, 1),        # 0! = 1
    (1, 1),        # 1! = 1
    (2, 2),        # 2! = 2
    (3, 6),        # 3! = 6
    (4, 24),       # 4! = 24
    (5, 120),      # 5! = 120
    (6, 720),      # 6! = 720
    (10, 3628800)  # 10! = 3628800
])
def test_factorial(input_value, expected_output):
    assert factorial(input_value) == expected_output

def test_factorial_negative():
    """Test that ValueError is raised for negative inputs."""
    with pytest.raises(ValueError):
        factorial(-1)