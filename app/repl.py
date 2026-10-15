
"""Interactive calculator REPL with design patterns and colors."""

import math

from colorama import Fore, init

from app.calculator import Calculator
from app.commands import registry
from app.observers import LoggingObserver, AutoSaveObserver


OPERATIONS = {
    "add", "subtract", "multiply", "divide",
    "power", "root", "modulus", "int_divide",
    "percent", "abs_diff",
}

ARITHMETIC_HELP = {
    "add 10 5": "Addition",
    "subtract 10 5": "Subtraction",
    "multiply 10 5": "Multiplication",
    "divide 10 5": "Division",
    "power 2 3": "Exponentiation",
    "root 16 2": "Root",
    "modulus 10 3": "Modulus",
    "int_divide 10 3": "Integer division",
    "percent 20 100": "Percentage",
    "abs_diff 10 5": "Absolute difference",
}


def main():
    """Run the interactive calculator."""
    init(autoreset=True)

    calculator = Calculator()
    config = calculator.config
    history = calculator.history

    calculator.add_observer(
        LoggingObserver(config.log_file)
    )

    if config.auto_save:
        calculator.add_observer(
            AutoSaveObserver(
                history,
                config.history_file
            )
        )

    def auto_save_history():
        """Update the automatic history CSV if enabled."""
        if config.auto_save:
            history.save_to_csv(config.history_file)

    print(Fore.CYAN + "Welcome to the Calculator!")
    print("Type 'help' for available commands.")

    while True:
        try:
            command = input("calculator> ").strip().lower()

            if command == "":
                continue

            # Decorator Pattern: commands registered dynamically.
            # Command Pattern: each class executes its own action.
            command_class = registry.get_command(command)

            if command_class is not None:
                try:
                    command_instance = command_class(calculator)
                    result = command_instance.execute()

                    if command == "help":
                        print(Fore.CYAN + "Available commands:")

                        for name, description in ARITHMETIC_HELP.items():
                            print(f"  {name} - {description}")

                        # Generated from registered command classes.
                        help_lines = registry.get_help().splitlines()

                        for line in help_lines[1:]:
                            print(line)

                    elif command == "history":
                        if result == "No calculations in history.":
                            print(Fore.YELLOW + result)
                        else:
                            print(Fore.CYAN + result)

                    elif command in {"undo", "redo"}:
                        if result.endswith("successful."):
                            auto_save_history()
                            print(Fore.GREEN + result)
                        else:
                            print(Fore.YELLOW + result)

                    elif command in {"clear", "load"}:
                        auto_save_history()
                        print(Fore.GREEN + result)

                    elif command == "exit":
                        print(Fore.CYAN + result)
                        break

                    else:
                        print(Fore.GREEN + result)

                except (
                    FileNotFoundError,
                    OSError,
                    ValueError,
                    KeyError,
                ) as error:
                    print(Fore.RED + f"Error: {error}")

                continue

            # Handle arithmetic operations.
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

                    print(Fore.GREEN + f"Result: {result}")

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
