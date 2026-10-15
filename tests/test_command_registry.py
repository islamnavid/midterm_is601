
"""Tests for decorator-based command registration."""

from app.command_registry import CommandRegistry
from app.operations import OperationFactory


def test_empty_registry():
    """An empty registry still displays available operations."""
    registry = CommandRegistry()

    assert registry.list_commands() == []
    assert registry.get_command("missing") is None

    help_text = registry.get_help()

    assert help_text.startswith("Available commands:")
    assert "Arithmetic operations:" in help_text
    assert "add number1 number2" in help_text


def test_register_command():
    registry = CommandRegistry()

    @registry.register("sample", "Sample command")
    class SampleCommand:
        pass

    assert registry.get_command("sample") is SampleCommand
    assert registry.list_commands() == ["sample"]
    assert "sample - Sample command" in registry.get_help()


def test_multiple_registered_commands():
    registry = CommandRegistry()

    @registry.register("first", "First command")
    class FirstCommand:
        pass

    @registry.register("second", "Second command")
    class SecondCommand:
        pass

    assert registry.get_command("first") is FirstCommand
    assert registry.get_command("second") is SecondCommand
    assert len(registry.list_commands()) == 2


def test_registered_command_replacement():
    registry = CommandRegistry()

    @registry.register("sample", "Original description")
    class OriginalCommand:
        pass

    @registry.register("sample", "Updated description")
    class UpdatedCommand:
        pass

    assert registry.get_command("sample") is UpdatedCommand
    assert len(registry.list_commands()) == 1
    assert "Updated description" in registry.get_help()


def test_help_includes_all_arithmetic_operations():
    """Help should list every operation defined in the factory."""
    registry = CommandRegistry()

    help_text = registry.get_help()

    expected_operations = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
        "modulus",
        "int_divide",
        "percent",
        "abs_diff",
    }

    assert set(OperationFactory.list_operations()) == (
        expected_operations
    )

    for operation in expected_operations:
        assert (
            f"  {operation} number1 number2"
            in help_text
        )


def test_help_updates_when_new_operation_is_added(monkeypatch):
    """Help should automatically include newly added operations."""
    registry = CommandRegistry()

    def double_sum(a, b):
        return 2 * (a + b)

    updated_operations = {
        **OperationFactory._operations,
        "double_sum": double_sum,
    }

    monkeypatch.setattr(
        OperationFactory,
        "_operations",
        updated_operations
    )

    assert "double_sum" in OperationFactory.list_operations()

    assert (
        OperationFactory.create_operation("double_sum")(2, 3)
        == 10
    )

    help_text = registry.get_help()

    assert "double_sum number1 number2" in help_text
