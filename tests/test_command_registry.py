
"""Tests for decorator-based command registration."""

from app.command_registry import CommandRegistry


def test_empty_registry():
    registry = CommandRegistry()

    assert registry.list_commands() == []
    assert registry.get_command("missing") is None
    assert registry.get_help() == "Available commands:"


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
