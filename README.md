# Enhanced Calculator Command-Line Application

## Project Overview

This project is an enhanced Python calculator developed for the IS601 Midterm Project.

The application provides an interactive command-line interface (REPL) for performing arithmetic calculations. It demonstrates object-oriented programming, multiple software design patterns, configurable application behavior, calculation history management, logging, CSV persistence, and automated testing.

## Features

- Basic and advanced arithmetic operations
- Factory Design Pattern for selecting arithmetic operations
- Memento Design Pattern for undo and redo functionality
- Observer Design Pattern for logging and automatic CSV saving
- Command Design Pattern for encapsulating calculator commands
- Decorator-based command registration and dynamic help generation
- Colorama for color-coded terminal output
- Calculation history management using pandas
- Manual CSV history saving and loading
- Environment-based configuration using python-dotenv
- Configurable calculation precision and history size
- Input validation and error handling
- Automated unit testing using pytest
- Test coverage reporting and enforcement using pytest-cov
- Continuous Integration using GitHub Actions

## Project Structure

```text
midterm_is601/
├── .github/
│   └── workflows/
│       └── python-app.yml
├── app/
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── command_registry.py
│   ├── commands.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── observers.py
│   ├── operations.py
│   └── repl.py
├── tests/
│   ├── __init__.py
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_command_registry.py
│   ├── test_commands.py
│   ├── test_configuration.py
│   ├── test_history.py
│   ├── test_memento.py
│   ├── test_observer.py
│   ├── test_operations.py
│   └── test_repl.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The `.env` file contains local configuration settings and is excluded from Git tracking.

The application may also generate `history/` and `logs/` directories for CSV files and logging output.

## Installation

Clone the GitHub repository:

```bash
git clone https://github.com/islamnavid/midterm_is601.git
cd midterm_is601
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment on macOS or Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

The project uses pandas, python-dotenv, pytest, pytest-cov, and colorama.

## Environment Configuration

Create a `.env` file in the project's root directory.

Example configuration:

```env
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=calculation_history.csv
```

Configuration settings control the history storage location, logging location, maximum history size, automatic saving, numeric precision, input limits, and file encoding.

The application uses the `CalculatorConfig` class to load and validate environment settings.

## Running the Calculator

Start the interactive calculator using:

```bash
python -m app.repl
```

The application displays an interactive prompt:

```text
calculator>
```

Users can enter arithmetic operations or history-management commands.

## Supported Arithmetic Operations

| Operation | Command | Description |
|---|---|---|
| Addition | `add` | Adds two numbers |
| Subtraction | `subtract` | Subtracts the second number |
| Multiplication | `multiply` | Multiplies two numbers |
| Division | `divide` | Divides the first number by the second |
| Power | `power` | Raises a number to a power |
| Root | `root` | Calculates a root |
| Modulus | `modulus` | Returns the remainder |
| Integer Division | `int_divide` | Performs integer division |
| Percentage | `percent` | Calculates a percentage |
| Absolute Difference | `abs_diff` | Calculates the absolute difference |

### Example Calculations

With the default precision of two decimal places:

```text
calculator> add 10 5
Result: 15.00

calculator> multiply 2.5 3
Result: 7.50

calculator> subtract 20 8
Result: 12.00
```

## History Management Commands

| Command | Description |
|---|---|
| `history` | Displays previous calculations |
| `undo` | Restores the previous history state |
| `redo` | Restores an undone history change |
| `clear` | Clears calculation history |
| `save` | Saves a manual CSV history backup |
| `load` | Loads a previously saved CSV history backup |
| `help` | Displays registered commands |
| `exit` | Exits the application |

### Example Session

```text
calculator> add 10 5
Result: 15.00

calculator> multiply 4 5
Result: 20.00

calculator> history
Calculation History:
add: 10.0, 5.0 = 15.0
multiply: 4.0, 5.0 = 20.0

calculator> undo
Undo successful.

calculator> redo
Redo successful.

calculator> save
History saved to history/manual_history.csv

calculator> clear
History cleared.

calculator> load
History loaded from history/manual_history.csv

calculator> exit
Goodbye!
```

## Design Patterns

### Factory Design Pattern

The Factory Design Pattern is implemented in `operations.py`.

It selects the appropriate arithmetic operation based on the operation name supplied by the user.

This separates operation selection from the calculator's core processing logic.

### Memento Design Pattern

The Memento Design Pattern is implemented using `calculator_memento.py` and `history.py`.

It allows the calculator to save snapshots of calculation history and restore previous states through undo and redo commands.

### Observer Design Pattern

The Observer Design Pattern is implemented using `observers.py`.

Registered observers respond to completed calculations, supporting logging and automatic history persistence.

This keeps those responsibilities separate from the calculator's core arithmetic functionality.

### Command Design Pattern

The Command Design Pattern is implemented in `commands.py`.

History management actions, including undo, redo, clear, save, and load, are represented as command objects.

This separates the command execution logic from the REPL interface.

### Decorator-Based Command Registration

The command registration system is implemented in `command_registry.py`.

Decorators register commands along with their descriptions.

The application uses this registration information to generate help output dynamically, reducing the need to maintain a separate hardcoded help list.

## Color-Coded Terminal Output

The application uses the Colorama library to improve readability.

Different terminal colors distinguish successful operations, calculation history, error messages, and other informational output.

## Calculation History and CSV Persistence

The application stores completed calculations in history.

Calculation history can be viewed, cleared, restored using undo/redo, and exported or imported using CSV files.

Pandas is used for CSV data handling.

Automatic saving is controlled through the application configuration, while the `save` and `load` commands support manual history backups.

## Logging and Error Handling

The application records completed calculations using its logging observer.

Logging locations and filenames can be configured through environment variables.

Input validation and exception handling help the calculator respond to invalid input, unsupported operations, and arithmetic errors without unexpectedly terminating the REPL.

## Automated Testing

The project uses pytest for automated unit testing.

Tests cover arithmetic operations, calculation history, configuration, design patterns, command execution, and REPL functionality.

Run all tests:

```bash
python -m pytest -q
```

Run tests with coverage reporting:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Enforce the required minimum of 90% code coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

### Latest Verified Local Test Results

- 101 automated tests passed
- 97.56% total code coverage
- Required minimum coverage: 90%

These results were recorded during development. Additional configuration tests have since been added.

## Continuous Integration

GitHub Actions automatically runs the project's test workflow when changes are pushed to the `main` branch or a pull request targets `main`.

The workflow installs dependencies, runs pytest, generates coverage results, and enforces the minimum 90% coverage requirement.

The workflow configuration is located at:

```text
.github/workflows/python-app.yml
```

The latest reported GitHub Actions run completed successfully.

## Git Version Control

Git is used to track development progress through incremental commits.

Changes are committed and pushed to GitHub as features, tests, and improvements are implemented.

The repository includes a `.gitignore` file to exclude local virtual environments, temporary files, generated output, and sensitive environment configuration.

## GitHub Repository

https://github.com/islamnavid/midterm_is601

## Development Status

The calculator implements the required arithmetic operations, history management, configuration, design patterns, logging, CSV persistence, automated testing, and continuous integration.

The project also includes the three optional enhancements: Command Pattern, decorator-based dynamic help, and Colorama terminal output.

Developed for the NJIT IS601 Midterm Project.