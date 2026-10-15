"""Interactive calculator REPL."""

from app.calculator import Calculator


def main():
    calculator = Calculator()

    print("Welcome to the Calculator!")
    print("Type 'help' for available commands.")

    operations = {
        "add", "subtract", "multiply", "divide",
        "power", "root", "modulus", "int_divide",
        "percent", "abs_diff",
    }

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
                print("  redo - Restore last undone calculation")
                print("  clear - Clear calculation history")
                print("  exit - Exit the calculator")

            elif command == "history":
                calculations = calculator.history.get_all()

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
                if calculator.history.undo():
                    print("Undo successful.")
                else:
                    print("Nothing to undo.")

            elif command == "redo":
                if calculator.history.redo():
                    print("Redo successful.")
                else:
                    print("Nothing to redo.")

            elif command == "clear":
                calculator.history.checkpoint()
                calculator.history.clear()
                print("History cleared.")

            elif command == "":
                continue

            else:
                parts = command.split()

                if parts[0] in operations:
                    if len(parts) != 3:
                        print("Usage: operation number1 number2")
                        continue

                    try:
                        operand1 = float(parts[1])
                        operand2 = float(parts[2])

                        result = calculator.calculate(
                            parts[0], operand1, operand2
                        )

                        print(f"Result: {result}")

                    except (ValueError, ZeroDivisionError) as error:
                        print(f"Error: {error}")

                else:
                    print(
                        "Unknown command. "
                        "Type 'help' for assistance."
                    )

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()