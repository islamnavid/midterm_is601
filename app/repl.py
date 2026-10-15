
"""Interactive calculator REPL with color-coded output."""

import math

from colorama import Fore, Style, init

from app.calculator import Calculator
from app.observers import LoggingObserver, AutoSaveObserver


OPERATIONS = {
    "add", "subtract", "multiply", "divide",
    "power", "root", "modulus", "int_divide",
    "percent", "abs_diff",
}


def main():
    """Run the interactive calculator."""

    # Initialize Colorama for colored terminal output.
    init(autoreset=True)

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

    # Register auto-save observer when enabled.
    if config.auto_save:
        calculator.add_observer(
            AutoSaveObserver(
                history,
                config.history_file
            )
        )

    def auto_save_history():
        """Save history when automatic saving is enabled."""
        if config.auto_save:
            history.save_to_csv(config.history_file)

    print(Fore.CYAN + "Welcome to the Calculator!")
    print("Type 'help' for available commands.")

    while True:
        try:
            command = input("calculator> ").strip().lower()

            if command == "exit":
                print(Fore.CYAN + "Goodbye!")
                break

            elif command == "help":
                print(Fore.CYAN + "Available commands:")
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
                    print(Fore.YELLOW + "No calculations in history.")
                else:
                    print(Fore.CYAN + "Calculation History:")

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
                    print(Fore.GREEN + "Undo successful.")
                else:
                    print(Fore.YELLOW + "Nothing to undo.")

            elif command == "redo":
                if history.redo():
                    auto_save_history()
                    print(Fore.GREEN + "Redo successful.")
                else:
                    print(Fore.YELLOW + "Nothing to redo.")

            elif command == "clear":
                # Save a checkpoint before clearing history.
                history.checkpoint()
                history.clear()

                auto_save_history()

                print(Fore.GREEN + "History cleared.")

            elif command == "save":
                try:
                    history.save_to_csv(manual_history_file)

                    print(
                        Fore.GREEN
                        + f"History saved to {manual_history_file}"
                    )

                except (OSError, ValueError) as error:
                    print(
                        Fore.RED
                        + f"Error saving history: {error}"
                    )

            elif command == "load":
                try:
                    # Remember the current history before loading.
                    previous_state = history.save_state()

                    history.load_from_csv(manual_history_file)

                    # Make loading reversible with undo.
                    history._undo_stack.append(previous_state)
                    history._redo_stack.clear()

                    auto_save_history()

                    print(
                        Fore.GREEN
                        + f"History loaded from {manual_history_file}"
                    )

                except (
                    FileNotFoundError,
                    OSError,
                    ValueError,
                    KeyError,
                ) as error:
                    print(
                        Fore.RED
                        + f"Error loading history: {error}"
                    )

            elif command == "":
                continue

            else:
                parts = command.split()

                if parts[0] in OPERATIONS:
                    if len(parts) != 3:
                        print(
                            Fore.YELLOW
                            + "Usage: operation number1 number2"
                        )
                        continue

                    try:
                        operand1 = float(parts[1])
                        operand2 = float(parts[2])

                        # Reject NaN and infinity.
                        if not (
                            math.isfinite(operand1)
                            and math.isfinite(operand2)
                        ):
                            raise ValueError(
                                "Inputs must be finite numbers."
                            )

                        # Enforce maximum input value.
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

                        print(
                            Fore.GREEN
                            + f"Result: {result}"
                        )

                    except (
                        ValueError,
                        ZeroDivisionError,
                        OverflowError,
                    ) as error:
                        print(Fore.RED + f"Error: {error}")

                else:
                    print(
                        Fore.RED
                        + "Unknown command. "
                        + "Type 'help' for assistance."
                    )

        except (KeyboardInterrupt, EOFError):
            print(Fore.CYAN + "\nGoodbye!")
            break

        except (OSError, ValueError) as error:
            print(Fore.RED + f"Error: {error}")


if __name__ == "__main__":
    main()
