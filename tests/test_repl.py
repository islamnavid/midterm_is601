"""Tests for the calculator REPL."""

import runpy
import warnings
from unittest.mock import patch

import pytest

from app.repl import main
from app.calculator_config import CalculatorConfig


def run_repl(commands, capsys):
    """Run the REPL with simulated user commands."""
    with patch("builtins.input", side_effect=commands):
        main()
    return capsys.readouterr().out


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 4, 5, 20),
        ("divide", 10, 2, 5),
        ("power", 2, 3, 8),
        ("modulus", 10, 3, 1),
    ],
)
def test_arithmetic_commands(operation, a, b, expected, capsys):
    output = run_repl(
        [f"{operation} {a} {b}", "exit"], capsys
    )
    assert f"Result: {float(expected)}" in output


def test_help(capsys):
    output = run_repl(["help", "exit"], capsys)
    assert "Available commands:" in output
    assert "history" in output
    assert "undo" in output


def test_history(capsys):
    output = run_repl(
        ["add 10 5", "history", "exit"], capsys
    )
    assert "add: 10.0, 5.0 = 15.0" in output


def test_empty_history(capsys):
    output = run_repl(["history", "exit"], capsys)
    assert "No calculations in history." in output


def test_undo_redo(capsys):
    output = run_repl(
        ["add 10 5", "undo", "redo", "exit"], capsys
    )
    assert "Undo successful." in output
    assert "Redo successful." in output


def test_undo_redo_empty(capsys):
    output = run_repl(["undo", "redo", "exit"], capsys)
    assert "Nothing to undo." in output
    assert "Nothing to redo." in output


def test_clear_history(capsys):
    output = run_repl(
        ["add 10 5", "clear", "history", "exit"], capsys
    )
    assert "History cleared." in output
    assert "No calculations in history." in output


def test_unknown_command(capsys):
    output = run_repl(["hello", "exit"], capsys)
    assert "Unknown command." in output


def test_invalid_arguments(capsys):
    output = run_repl(["add 10", "exit"], capsys)
    assert "Usage: operation number1 number2" in output


def test_invalid_number(capsys):
    output = run_repl(["add abc 5", "exit"], capsys)
    assert "Error:" in output


def test_division_by_zero(capsys):
    output = run_repl(["divide 10 0", "exit"], capsys)
    assert "Error:" in output


def test_empty_command(capsys):
    output = run_repl(["", "exit"], capsys)
    assert "Goodbye!" in output


def test_keyboard_interrupt(capsys):
    output = run_repl(
        [KeyboardInterrupt()], capsys
    )
    assert "Goodbye!" in output


def test_eof(capsys):
    output = run_repl([EOFError()], capsys)
    assert "Goodbye!" in output


@pytest.fixture
def isolated_log_file(tmp_path, monkeypatch):
    """Redirect calculator logging to a temporary test file."""
    log_file = tmp_path / "calculator.log"

    original_init = CalculatorConfig.__init__

    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.log_file = log_file
        self.auto_save = False

    monkeypatch.setattr(
        CalculatorConfig,
        "__init__",
        patched_init
    )

    return log_file


def test_repl_logs_successful_calculation(
    capsys, isolated_log_file
):
    """Successful calculations should produce INFO logs."""
    run_repl(["add 10 5", "exit"], capsys)

    log_content = isolated_log_file.read_text(
        encoding="utf-8"
    )

    assert "INFO" in log_content
    assert "add: 10.0, 5.0 = 15.0" in log_content


def test_repl_logs_division_by_zero(
    capsys, isolated_log_file
):
    """Division by zero should produce an ERROR log."""
    run_repl(["divide 10 0", "exit"], capsys)

    log_content = isolated_log_file.read_text(
        encoding="utf-8"
    )

    assert "ERROR" in log_content
    assert "Cannot divide by zero" in log_content


def test_repl_logs_invalid_operand_count(
    capsys, isolated_log_file
):
    """Missing operands should produce a WARNING log."""
    run_repl(["add 10", "exit"], capsys)

    log_content = isolated_log_file.read_text(
        encoding="utf-8"
    )

    assert "WARNING" in log_content
    assert "Invalid number of operands" in log_content


def test_repl_logs_unknown_command(
    capsys, isolated_log_file
):
    """Unknown commands should produce a WARNING log."""
    run_repl(["unknown", "exit"], capsys)

    log_content = isolated_log_file.read_text(
        encoding="utf-8"
    )

    assert "WARNING" in log_content
    assert "Unknown command: unknown" in log_content


def test_repl_logs_invalid_number(
    capsys, isolated_log_file
):
    """Invalid numeric input should produce an ERROR log."""
    run_repl(["add abc 5", "exit"], capsys)

    log_content = isolated_log_file.read_text(
        encoding="utf-8"
    )

    assert "ERROR" in log_content
    assert "could not convert string to float" in log_content


@pytest.mark.parametrize(
    "error_type",
    [ValueError, FileNotFoundError, OSError],
)
def test_registered_command_error_is_handled(
    error_type, capsys, isolated_log_file
):
    """Command failures should be reported, logged, and not stop the REPL."""
    from app.repl import registry

    class FailingCommand:
        def __init__(self, calculator):
            self.calculator = calculator

        def execute(self):
            raise error_type("Simulated command failure")

    original_get_command = registry.get_command

    def get_command(name):
        if name == "broken":
            return FailingCommand
        return original_get_command(name)

    with patch.object(registry, "get_command", side_effect=get_command):
        output = run_repl(["broken", "exit"], capsys)

    assert "Error: Simulated command failure" in output
    assert "Goodbye!" in output
    log_content = isolated_log_file.read_text(encoding="utf-8")
    assert "ERROR" in log_content
    assert "Simulated command failure" in log_content


def test_module_entry_point(capsys, isolated_log_file):
    """Running the REPL as __main__ should start and exit cleanly."""
    with patch("builtins.input", side_effect=["exit"]):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r".*app\.repl.*found in sys\.modules.*",
                category=RuntimeWarning,
            )
            runpy.run_module("app.repl", run_name="__main__")

    output = capsys.readouterr().out
    assert "Welcome to the Calculator!" in output
    assert "Goodbye!" in output
