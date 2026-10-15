
"""Tests for calculator input validation."""

import math

import pytest

from app.calculator import Calculator
from app.exceptions import ValidationError
from app.input_validators import validate_number


@pytest.mark.parametrize("value", [
    0, 10, -10, 1000000, -1000000, 2.5
])
def test_valid_numbers(value):
    assert validate_number(value, 1000000) == value


@pytest.mark.parametrize("value", [
    "abc", None, True, False, [], {}
])
def test_invalid_types(value):
    with pytest.raises(ValidationError):
        validate_number(value, 1000000)


@pytest.mark.parametrize("value", [
    math.inf, -math.inf, math.nan
])
def test_non_finite_numbers(value):
    with pytest.raises(ValidationError):
        validate_number(value, 1000000)


@pytest.mark.parametrize("value", [
    1000001, -1000001
])
def test_out_of_range_numbers(value):
    with pytest.raises(ValidationError):
        validate_number(value, 1000000)


def test_calculator_rejects_out_of_range_input():
    calculator = Calculator()

    with pytest.raises(ValidationError):
        calculator.calculate("add", 1000001, 5)

    assert calculator.history.count() == 0


def test_failed_calculation_does_not_change_history():
    calculator = Calculator()

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.calculate("divide", 10, 0)

    assert calculator.history.count() == 0
