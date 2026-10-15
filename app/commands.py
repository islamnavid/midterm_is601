
"""Command Pattern implementation for calculator commands."""

from app.command_registry import CommandRegistry


registry = CommandRegistry()


class Command:
    """Base class for calculator commands."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        """Execute the command."""
        raise NotImplementedError(
            "Subclasses must implement execute()."
        )


@registry.register("history", "Show calculation history")
class HistoryCommand(Command):
    """Display saved calculations."""

    def execute(self):
        calculations = self.calculator.history.get_all()

        if not calculations:
            return "No calculations in history."

        lines = ["Calculation History:"]

        for calculation in calculations:
            lines.append(
                f"{calculation.operation}: "
                f"{calculation.operand1}, "
                f"{calculation.operand2} = "
                f"{calculation.result}"
            )

        return "\n".join(lines)


@registry.register("undo", "Undo the last history change")
class UndoCommand(Command):
    """Undo a history change."""

    def execute(self):
        if self.calculator.history.undo():
            return "Undo successful."

        return "Nothing to undo."


@registry.register("redo", "Restore an undone history change")
class RedoCommand(Command):
    """Redo a history change."""

    def execute(self):
        if self.calculator.history.redo():
            return "Redo successful."

        return "Nothing to redo."


@registry.register("clear", "Clear calculation history")
class ClearCommand(Command):
    """Clear calculation history."""

    def execute(self):
        # The history class creates its own undo checkpoint.
        self.calculator.history.clear()
        return "History cleared."


@registry.register("save", "Save a manual history backup")
class SaveCommand(Command):
    """Save calculation history to CSV."""

    def execute(self):
        path = (
            self.calculator.config.history_dir
            / "manual_history.csv"
        )

        self.calculator.history.save_to_csv(path)
        return f"History saved to {path}"


@registry.register("load", "Load a manual history backup")
class LoadCommand(Command):
    """Load calculation history from CSV."""

    def execute(self):
        path = (
            self.calculator.config.history_dir
            / "manual_history.csv"
        )

        # load_from_csv() already saves the previous state
        # for undo and clears the redo stack.
        self.calculator.history.load_from_csv(path)

        return f"History loaded from {path}"


@registry.register("help", "Show available commands")
class HelpCommand(Command):
    """Display dynamically generated help."""

    def execute(self):
        return registry.get_help()


@registry.register("exit", "Exit the calculator")
class ExitCommand(Command):
    """Represent the exit command."""

    def execute(self):
        return "Goodbye!"
