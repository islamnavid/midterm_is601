"""Tests for the calculator REPL."""

from unittest.mock import patch

import pytest

from app.repl import main


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