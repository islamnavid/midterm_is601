
"""Interactive calculator REPL."""

import math

from app.calculator import Calculator
from app.observers import LoggingObserver, AutoSaveObserver


OPERATIONS = {
    "add", "subtract", "multiply", "divide",
    "power", "root", "modulus", "int_divide",
    "percent", "abs_diff",
}


def main():
    """Run the interactive calculator."""
    calculator = Calculator()
    config = calculator.config
    history = calculator.history

    # Separate manual backup from automatic history.
    manual_history_file = (
        config.history_dir / "manual_history.csv"
    )

    # Register logging observer.
    calculator.add_observer(
        LoggingObserver(config.log_file)
    )

    # Register auto-save observer if enabled.
    if config.auto_save:
        calculator.add_observer(
            AutoSaveObserver(
                history,
                config.history_file
            )
        )

    def auto_save_history():
        """Save current history when auto-save is enabled."""
        if config.auto_save:
            history.save_to_csv(config.history_file)

    print("Welcome to the Calculator!")
    print("Type 'help' for available commands.")

    while True:
        try:
            command = input("calculator> ").strip().lower()

            if command == "exit":
                print("Goodbye!")
                break

            elif command == "help":
                print("Available commands:")
                print("  add 10 5 - Addition")
                print("  subtract 10 5 - Subtraction")
                print("  multiply 10 5 - Multiplication")
                print("  divide 10 5 - Division")
                print("  power 2 3 - Exponentiation")
                print("  root 16 2 - Root")
                print("  modulus 10 3 - Modulus")
                print("  int_divide 10 3 - Integer division")
                print("  percent 20 100 - Percentage")
                print("  abs_diff 10 5 - Absolute difference")
                print("  history - Show calculation history")
                print("  undo - Undo last calculation")
                print("  redo - Restore undone calculation")
                print("  clear - Clear calculation history")
                print("  save - Save manual history backup")
                print("  load - Load manual history backup")
                print("  help - Show available commands")
                print("  exit - Exit the calculator")

            elif command == "history":
                calculations = history.get_all()

                if not calculations:
                    print("No calculations in history.")
                else:
                    for calculation in calculations:
                        print(
                            f"{calculation.operation}: "
                            f"{calculation.operand1}, "
                            f"{calculation.operand2} = "
                            f"{calculation.result}"
                        )

            elif command == "undo":
                if history.undo():
                    auto_save_history()
                    print("Undo successful.")
                else:
                    print("Nothing to undo.")

            elif command == "redo":
                if history.redo():
                    auto_save_history()
                    print("Redo successful.")
                else:
                    print("Nothing to redo.")

            elif command == "clear":
                # Checkpoint is handled here, not in clear().
                history.checkpoint()
                history.clear()
                auto_save_history()
                print("History cleared.")

            elif command == "save":
                try:
                    history.save_to_csv(manual_history_file)
                    print(
                        f"History saved to {manual_history_file}"
                    )
                except (OSError, ValueError) as error:
                    print(f"Error saving history: {error}")

            elif command == "load":
                try:
                    # Save state before replacing history.
                    previous_state = history.save_state()

                    history.load_from_csv(manual_history_file)

                    # Allow undo to restore the previous history.
                    history._undo_stack.append(previous_state)
                    history._redo_stack.clear()

                    auto_save_history()

                    print(
                        f"History loaded from {manual_history_file}"
                    )

                except (
                    FileNotFoundError,
                    OSError,
                    ValueError,
                    KeyError,
                ) as error:
                    print(f"Error loading history: {error}")

            elif command == "":
                continue

            else:
                parts = command.split()

                if parts[0] in OPERATIONS:
                    if len(parts) != 3:
                        print("Usage: operation number1 number2")
                        continue

                    try:
                        operand1 = float(parts[1])
                        operand2 = float(parts[2])

                        if not (
                            math.isfinite(operand1)
                            and math.isfinite(operand2)
                        ):
                            raise ValueError(
                                "Inputs must be finite numbers."
                            )

                        if (
                            abs(operand1) > config.max_input_value
                            or abs(operand2) > config.max_input_value
                        ):
                            raise ValueError(
                                "Input exceeds maximum allowed value."
                            )

                        result = calculator.calculate(
                            parts[0],
                            operand1,
                            operand2
                        )

                        print(f"Result: {result}")

                    except (
                        ValueError,
                        ZeroDivisionError,
                        OverflowError,
                    ) as error:
                        print(f"Error: {error}")

                else:
                    print(
                        "Unknown command. "
                        "Type 'help' for assistance."
                    )

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        except (OSError, ValueError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
