
"""Interactive calculator REPL with Command Pattern and Colorama."""

from colorama import Fore, Style, init

from app.calculator import Calculator
from app.commands import registry
from app.observers import LoggingObserver, AutoSaveObserver

init(autoreset=True)


def main():
    """Run the interactive calculator."""

    calculator = Calculator()

    # Register the logging observer.
    calculator.add_observer(
        LoggingObserver(
            log_file=calculator.config.log_file
        )
    )

    # Register automatic history saving if enabled.
    if calculator.config.auto_save:
        calculator.add_observer(
            AutoSaveObserver(
                history=calculator.history,
                file_path=calculator.config.history_file
            )
        )

    operations = {
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

    print(
        Fore.CYAN
        + "Welcome to the Calculator!"
        + Style.RESET_ALL
    )
    print("Type 'help' for available commands.")

    while True:
        try:
            user_input = input("calculator> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command_name = parts[0].lower()

            # Execute registered commands.
            command_class = registry.get_command(command_name)

            if command_class is not None:
                try:
                    command = command_class(calculator)
                    result = command.execute()

                    if command_name == "history":
                        print(
                            Fore.CYAN
                            + str(result)
                            + Style.RESET_ALL
                        )

                    elif command_name == "help":
                        print(
                            Fore.CYAN
                            + str(result)
                            + Style.RESET_ALL
                        )

                    else:
                        print(
                            Fore.GREEN
                            + str(result)
                            + Style.RESET_ALL
                        )

                    if command_name == "exit":
                        break

                except (
                    ValueError,
                    FileNotFoundError,
                    OSError,
                ) as error:
                    print(
                        Fore.RED
                        + f"Error: {error}"
                        + Style.RESET_ALL
                    )

                continue

            # Execute arithmetic operations.
            if command_name in operations:

                if len(parts) != 3:
                    print(
                        Fore.RED
                        + "Usage: operation number1 number2"
                        + Style.RESET_ALL
                    )
                    continue

                try:
                    operand1 = float(parts[1])
                    operand2 = float(parts[2])

                    result = calculator.calculate(
                        command_name,
                        operand1,
                        operand2
                    )

                    # Format result using CALCULATOR_PRECISION.
                    formatted_result = calculator.format_result(
                        result
                    )

                    print(
                        Fore.GREEN
                        + f"Result: {formatted_result}"
                        + Style.RESET_ALL
                    )

                except (
                    ValueError,
                    ZeroDivisionError,
                    OverflowError,
                ) as error:
                    print(
                        Fore.RED
                        + f"Error: {error}"
                        + Style.RESET_ALL
                    )

            else:
                print(
                    Fore.RED
                    + "Unknown command. "
                    + "Type 'help' for assistance."
                    + Style.RESET_ALL
                )

        except (KeyboardInterrupt, EOFError):
            print(
                "\n"
                + Fore.CYAN
                + "Goodbye!"
                + Style.RESET_ALL
            )
            break


if __name__ == "__main__":
    main()
