import pytest

from app.operations import (
    add,
    subtract,
    multiply,
    divide,
    power,
    root,
    modulus,
    int_divide,
    percent,
    abs_diff,
)

@pytest.mark.parametrize(
    "operation,a,b",
    [
        (add, 1e308, 1e308),
        (subtract, -1e308, 1e308),
        (multiply, 1e308, 10),
        (divide, 1e308, 1e-308),
        (power, 10, 1000),
        (root, 0, -2),
        (percent, 1e308, 1e-308),
        (abs_diff, 1e308, -1e308),
    ],
)
def test_overflow_and_invalid_results(operation, a, b):
    with pytest.raises(ValueError):
        operation(a, b)


@pytest.mark.parametrize("invalid", [
    float("inf"),
    float("-inf"),
    float("nan"),
])
def test_non_finite_inputs(invalid):
    with pytest.raises(ValueError):
        add(invalid, 5)


def test_zero_with_negative_exponent():
    with pytest.raises(ValueError):
        power(0, -2)


def test_valid_large_calculation():
    assert multiply(1e100, 2) == pytest.approx(2e100)
