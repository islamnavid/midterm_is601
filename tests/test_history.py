
"""Unit tests for calculation history management."""

from app.calculation import Calculation
from app.history import CalculationHistory


def test_empty_history():
    history = CalculationHistory()

    assert history.count() == 0
    assert history.get_all() == []
    assert history.get_last() is None


def test_add_calculation():
    history = CalculationHistory()
    calculation = Calculation("add", 10, 5)

    history.add(calculation)

    assert history.count() == 1
    assert history.get_last().result == 15


def test_multiple_calculations():
    history = CalculationHistory()

    history.add(Calculation("add", 10, 5))
    history.add(Calculation("multiply", 4, 5))

    assert history.count() == 2
    assert history.get_last().result == 20


def test_get_all_calculations():
    history = CalculationHistory()

    first = Calculation("add", 10, 5)
    second = Calculation("subtract", 10, 3)

    history.add(first)
    history.add(second)

    calculations = history.get_all()

    assert len(calculations) == 2
    assert calculations[0].result == 15
    assert calculations[1].result == 7


def test_get_all_returns_copy():
    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))

    calculations = history.get_all()
    calculations.clear()

    assert history.count() == 1


def test_clear_history():
    history = CalculationHistory()

    history.add(Calculation("add", 10, 5))
    history.add(Calculation("multiply", 4, 5))

    history.clear()

    assert history.count() == 0
    assert history.get_all() == []
    assert history.get_last() is None
