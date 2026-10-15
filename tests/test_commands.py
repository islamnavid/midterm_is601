
"""Tests for the calculator Command Pattern."""

import pytest

from app.calculator import Calculator
from app.commands import (
    Command,
    registry,
    HistoryCommand,
    UndoCommand,
    RedoCommand,
    ClearCommand,
    SaveCommand,
    LoadCommand,
    HelpCommand,
    ExitCommand,
)


@pytest.fixture
def calculator(tmp_path):
    """Create a calculator with isolated history storage."""
    calc = Calculator()
    calc.config.history_dir = tmp_path
    return calc


def test_base_command(calculator):
    command = Command(calculator)

    with pytest.raises(NotImplementedError):
        command.execute()


def test_registered_commands():
    expected = {
        "history", "undo", "redo", "clear",
        "save", "load", "help", "exit",
    }

    assert expected.issubset(set(registry.list_commands()))

    for name in expected:
        assert registry.get_command(name) is not None


def test_empty_history(calculator):
    result = HistoryCommand(calculator).execute()
    assert result == "No calculations in history."


def test_history_with_calculations(calculator):
    calculator.calculate("add", 10, 5)

    result = HistoryCommand(calculator).execute()

    assert "Calculation History:" in result
    assert "add:" in result
    assert "15" in result



def test_undo_without_history(calculator):
    result = UndoCommand(calculator).execute()
    assert result == "Nothing to undo."


def test_redo_without_history(calculator):
    result = RedoCommand(calculator).execute()
    assert result == "Nothing to redo."


def test_undo_and_redo(calculator):
    calculator.calculate("add", 10, 5)

    assert calculator.history.count() == 1

    assert UndoCommand(calculator).execute() == (
        "Undo successful."
    )
    assert calculator.history.count() == 0

    assert RedoCommand(calculator).execute() == (
        "Redo successful."
    )
    assert calculator.history.count() == 1


def test_clear_command(calculator):
    calculator.calculate("add", 10, 5)

    result = ClearCommand(calculator).execute()

    assert result == "History cleared."
    assert calculator.history.count() == 0

    assert UndoCommand(calculator).execute() == (
        "Undo successful."
    )
    assert calculator.history.count() == 1


def test_save_command(calculator, tmp_path):
    calculator.calculate("add", 10, 5)

    result = SaveCommand(calculator).execute()

    file_path = tmp_path / "manual_history.csv"

    assert file_path.exists()
    assert "History saved to" in result


def test_load_command(calculator):
    calculator.calculate("add", 10, 5)

    SaveCommand(calculator).execute()
    ClearCommand(calculator).execute()

    assert calculator.history.count() == 0

    result = LoadCommand(calculator).execute()

    assert "History loaded from" in result
    assert calculator.history.count() == 1


def test_undo_after_load(calculator):
    calculator.calculate("add", 10, 5)
    SaveCommand(calculator).execute()

    ClearCommand(calculator).execute()
    LoadCommand(calculator).execute()

    assert UndoCommand(calculator).execute() == (
        "Undo successful."
    )
    assert calculator.history.count() == 0


def test_load_missing_file(calculator):
    with pytest.raises(FileNotFoundError):
        LoadCommand(calculator).execute()


def test_help_command(calculator):
    result = HelpCommand(calculator).execute()

    assert "Available commands:" in result
    assert "history" in result
    assert "undo" in result
    assert "save" in result


def test_exit_command(calculator):
    result = ExitCommand(calculator).execute()

    assert result == "Goodbye!"
