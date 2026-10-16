
"""Unit tests for calculation history management."""

import pandas as pd
import pytest

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


def test_save_and_load_csv(tmp_path):
    """Verify calculation history can be saved and loaded."""
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
    """Verify empty history can be saved and loaded."""
    file_path = tmp_path / "empty.csv"

    history = CalculationHistory()
    history.save_to_csv(file_path)

    assert file_path.exists()

    loaded_history = CalculationHistory()
    loaded_history.load_from_csv(file_path)

    assert loaded_history.count() == 0


def test_save_csv_creates_directory(tmp_path):
    """Verify missing directories are created automatically."""
    file_path = tmp_path / "data" / "history.csv"

    history = CalculationHistory()
    history.add(Calculation("subtract", 10, 3))

    history.save_to_csv(file_path)

    assert file_path.exists()


def test_load_missing_csv(tmp_path):
    """Verify missing CSV files raise an error."""
    file_path = tmp_path / "missing.csv"

    history = CalculationHistory()

    with pytest.raises(FileNotFoundError):
        history.load_from_csv(file_path)


def test_load_invalid_csv(tmp_path):
    """Verify CSV files with missing columns are rejected."""
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("name,value\nexample,10\n")

    history = CalculationHistory()

    with pytest.raises(ValueError, match="Invalid history CSV format"):
        history.load_from_csv(file_path)


def test_csv_preserves_timestamp(tmp_path):
    """Verify timestamps survive CSV serialization."""
    file_path = tmp_path / "timestamps.csv"

    history = CalculationHistory()
    calculation = Calculation("add", 10, 5)
    history.add(calculation)

    history.save_to_csv(file_path)

    loaded_history = CalculationHistory()
    loaded_history.load_from_csv(file_path)

    assert loaded_history.get_last().timestamp == calculation.timestamp


def test_csv_has_required_columns(tmp_path):
    """Verify saved CSV files contain all required columns."""
    file_path = tmp_path / "history.csv"

    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))
    history.save_to_csv(file_path)

    dataframe = pd.read_csv(file_path)

    assert list(dataframe.columns) == [
        "operation",
        "operand1",
        "operand2",
        "result",
        "timestamp",
    ]


def test_load_empty_file(tmp_path):
    """Reject completely empty CSV files."""
    file_path = tmp_path / "empty_file.csv"
    file_path.write_text("")

    history = CalculationHistory()

    with pytest.raises(ValueError, match="Invalid history CSV format"):
        history.load_from_csv(file_path)


@pytest.mark.parametrize(
    "column,value",
    [
        ("operation", "unknown"),
        ("operand1", "abc"),
        ("operand2", "abc"),
        ("result", "abc"),
        ("result", "999"),
        ("timestamp", "not-a-date"),
        ("timestamp", ""),
        ("operand1", "nan"),
        ("operand2", "inf"),
        ("result", "inf"),
    ],
)
def test_load_corrupted_csv(tmp_path, column, value):
    """Reject corrupted CSV records without modifying history."""
    file_path = tmp_path / "corrupted.csv"

    original = Calculation("add", 10, 5)
    row = original.to_dict()
    row[column] = value

    pd.DataFrame([row]).to_csv(file_path, index=False)

    history = CalculationHistory()
    history.add(Calculation("multiply", 3, 4))

    with pytest.raises(ValueError, match="Invalid history CSV format"):
        history.load_from_csv(file_path)

    assert history.count() == 1
    assert history.get_last().result == 12


def test_failed_load_preserves_undo_stack(tmp_path):
    """Verify failed CSV loading does not create undo checkpoints."""
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("invalid,data\n1,2\n")

    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))

    with pytest.raises(ValueError):
        history.load_from_csv(file_path)

    assert history.undo() is False
    assert history.count() == 1


def test_load_respects_maximum_history_size(tmp_path):
    """Verify CSV loading enforces the configured history limit."""
    file_path = tmp_path / "history.csv"

    source = CalculationHistory()

    for number in range(5):
        source.add(Calculation("add", number, 1))

    source.save_to_csv(file_path)

    loaded = CalculationHistory(max_history_size=2)
    loaded.load_from_csv(file_path)

    assert loaded.count() == 2
    assert loaded.get_all()[0].operand1 == 3
    assert loaded.get_all()[1].operand1 == 4


def test_undo_after_successful_load(tmp_path):
    """Verify a successful CSV load can be undone."""
    file_path = tmp_path / "history.csv"

    source = CalculationHistory()
    source.add(Calculation("add", 10, 5))
    source.save_to_csv(file_path)

    history = CalculationHistory()
    history.add(Calculation("multiply", 3, 4))

    history.load_from_csv(file_path)

    assert history.get_last().result == 15

    assert history.undo() is True
    assert history.get_last().result == 12
