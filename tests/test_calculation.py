
"""Unit tests for the Calculation class."""

from datetime import datetime

import pytest

from app.calculation import Calculation


@pytest.mark.parametrize(
    "operation,a,b,expected",
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
def test_calculation_result(operation, a, b, expected):
    """Verify that calculations produce correct results."""
    calculation = Calculation(operation, a, b)
    assert calculation.result == pytest.approx(expected)


def test_calculation_timestamp():
    """Verify that each calculation has a timestamp."""
    calculation = Calculation("add", 10, 5)
    assert isinstance(calculation.timestamp, datetime)


def test_calculation_to_dict():
    """Verify that calculations can be converted to dictionaries."""
    calculation = Calculation("multiply", 4, 5)
    data = calculation.to_dict()

    assert data["operation"] == "multiply"
    assert data["operand1"] == 4
    assert data["operand2"] == 5
    assert data["result"] == 20
    assert isinstance(data["timestamp"], str)


def test_calculation_invalid_operation():
    """Verify that unsupported operations raise an error."""
    with pytest.raises(ValueError, match="Unsupported operation"):
        Calculation("unknown", 10, 5)


def test_calculation_division_by_zero():
    """Verify that division by zero is handled."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Calculation("divide", 10, 0)
