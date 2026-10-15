
"""Unit tests for the Calculator class."""

from unittest.mock import Mock

import pytest

from app.calculator import Calculator
from app.exceptions import ValidationError


@pytest.fixture
def calculator():
    """Create a fresh calculator for each test."""
    return Calculator()


def test_calculator_initialization(calculator):
    """Verify configuration, history, and observers are initialized."""
    assert calculator.config is not None
    assert calculator.history is not None
    assert calculator.history.count() == 0
    assert calculator.observers == []


def test_history_limit_uses_configuration(calculator):
    """Verify history uses the configured maximum size."""
    assert (
        calculator.history.max_history_size
        == calculator.config.max_history_size
    )


def test_add_observer(calculator):
    """Verify an observer can be registered."""
    observer = Mock()

    calculator.add_observer(observer)

    assert observer in calculator.observers


def test_notify_observers(calculator):
    """Verify all registered observers receive calculations."""
    observer1 = Mock()
    observer2 = Mock()

    calculator.add_observer(observer1)
    calculator.add_observer(observer2)

    calculator.calculate("add", 10, 5)

    observer1.update.assert_called_once()
    observer2.update.assert_called_once()

    calculation = observer1.update.call_args.args[0]

    assert calculation.operation == "add"
    assert calculation.result == 15


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
def test_calculator_operations(calculator, operation, a, b, expected):
    """Verify calculations return results and update history."""
    result = calculator.calculate(operation, a, b)

    assert result == pytest.approx(expected)
    assert calculator.history.count() == 1


def test_multiple_calculations_update_history(calculator):
    """Verify successful calculations accumulate in history."""
    calculator.calculate("add", 10, 5)
    calculator.calculate("multiply", 4, 5)

    assert calculator.history.count() == 2


def test_invalid_operation_does_not_change_history(calculator):
    """Verify unsupported operations do not modify history."""
    with pytest.raises(ValueError, match="Unsupported operation"):
        calculator.calculate("unknown", 10, 5)

    assert calculator.history.count() == 0


def test_invalid_input_does_not_notify_observers(calculator):
    """Verify invalid inputs do not notify observers."""
    observer = Mock()
    calculator.add_observer(observer)

    with pytest.raises(ValidationError):
        calculator.calculate("add", "invalid", 5)

    observer.update.assert_not_called()
    assert calculator.history.count() == 0


def test_division_by_zero_does_not_notify_observers(calculator):
    """Verify failed arithmetic does not notify observers."""
    observer = Mock()
    calculator.add_observer(observer)

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.calculate("divide", 10, 0)

    observer.update.assert_not_called()
    assert calculator.history.count() == 0


def test_format_result(calculator):
    """Verify results use the configured decimal precision."""
    calculator.config.precision = 2

    assert calculator.format_result(10) == "10.00"
    assert calculator.format_result(3.14159) == "3.14"


def test_successful_calculation_creates_checkpoint(calculator):
    """Verify successful calculations create undo checkpoints."""
    calculator.calculate("add", 10, 5)

    assert calculator.history.count() == 1

    calculator.history.undo()

    assert calculator.history.count() == 0
