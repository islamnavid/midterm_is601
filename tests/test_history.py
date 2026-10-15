
"""Unit tests for calculation history management."""

from app.calculation import Calculation
from app.history import CalculationHistory
import pytest

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

def test_save_and_load_csv(tmp_path):
    """Verify that calculation history can be saved and loaded."""
    file_path = tmp_path / "history.csv"

    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))
    history.add(Calculation("multiply", 4, 5))

    history.save_to_csv(file_path)

    assert file_path.exists()

    loaded_history = CalculationHistory()
    loaded_history.load_from_csv(file_path)

    assert loaded_history.count() == 2
    assert loaded_history.get_all()[0].result == 15
    assert loaded_history.get_last().result == 20


def test_save_empty_history(tmp_path):
    """Verify that empty history can be saved and loaded."""
    file_path = tmp_path / "empty.csv"

    history = CalculationHistory()
    history.save_to_csv(file_path)

    assert file_path.exists()

    loaded_history = CalculationHistory()
    loaded_history.load_from_csv(file_path)

    assert loaded_history.count() == 0


def test_save_csv_creates_directory(tmp_path):
    """Verify that missing directories are created automatically."""
    file_path = tmp_path / "data" / "history.csv"

    history = CalculationHistory()
    history.add(Calculation("subtract", 10, 3))

    history.save_to_csv(file_path)

    assert file_path.exists()


def test_load_missing_csv(tmp_path):
    """Verify that a missing CSV file raises an error."""
    file_path = tmp_path / "missing.csv"

    history = CalculationHistory()

    with pytest.raises(FileNotFoundError):
        history.load_from_csv(file_path)


def test_load_invalid_csv(tmp_path):
    """Verify that an invalid CSV format is rejected."""
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("name,value\nexample,10\n")

    history = CalculationHistory()

    with pytest.raises(ValueError, match="Invalid history CSV format"):
        history.load_from_csv(file_path)


def test_csv_preserves_timestamp(tmp_path):
    """Verify that timestamps are preserved after loading."""
    file_path = tmp_path / "timestamps.csv"

    history = CalculationHistory()
    calculation = Calculation("add", 10, 5)
    history.add(calculation)

    history.save_to_csv(file_path)

    loaded_history = CalculationHistory()
    loaded_history.load_from_csv(file_path)

    loaded_calculation = loaded_history.get_last()

    assert loaded_calculation.timestamp == calculation.timestamp
