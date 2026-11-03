
"""Tests for calculator arithmetic operations."""

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
    "operation,a,b,expected",
    [
        (add, 10, 5, 15),
        (subtract, 10, 5, 5),
        (multiply, 10, 5, 50),
        (divide, 10, 5, 2),
        (power, 2, 3, 8),
        (root, 16, 2, 4),
        (modulus, 10, 3, 1),
        (int_divide, 10, 3, 3),
        (percent, 25, 100, 25),
        (abs_diff, 5, 12, 7),
    ],
)
def test_operations(operation, a, b, expected):
    assert operation(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "operation",
    [divide, modulus, int_divide, percent],
)
def test_zero_division(operation):
    with pytest.raises(ValueError):
        operation(10, 0)


def test_root_with_zero_degree():
    with pytest.raises(ValueError):
        root(16, 0)


def test_root_with_negative_number():
    assert root(-27, 3) == pytest.approx(-3)


def test_invalid_even_root():
    with pytest.raises(ValueError):
        root(-16, 2)


def test_negative_exponent():
    assert power(2, -2) == pytest.approx(0.25)


def test_invalid_complex_power():
    with pytest.raises(ValueError):
        power(-4, 0.5)

from app.operations import OperationFactory


@pytest.mark.parametrize(
    "operation_name,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("root", 16, 2, 4),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 5, 12, 7),
    ],
)
def test_operation_factory(operation_name, a, b, expected):
    """Verify that the Factory selects the correct operation."""
    operation = OperationFactory.create_operation(operation_name)
    assert operation(a, b) == pytest.approx(expected)


def test_operation_factory_invalid_name():
    """Verify that unsupported operations raise an error."""
    with pytest.raises(ValueError, match="Unsupported operation"):
        OperationFactory.create_operation("unknown")


def test_operation_factory_case_insensitive():
    """Verify that operation names are case-insensitive."""
    operation = OperationFactory.create_operation("ADD")
    assert operation(10, 5) == 15


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

