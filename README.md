# Enhanced Calculator Command-Line Application

## Project Overview

This project is an enhanced Python calculator developed for the **NJIT IS601 Midterm Project**.

The application provides an interactive command-line interface (REPL) for performing basic and advanced arithmetic calculations. It demonstrates object-oriented programming, software design patterns, environment-based configuration, calculation history management, logging, CSV persistence, error handling, and automated testing.

The project also includes three optional enhancements: the Command Design Pattern, decorator-based dynamic help, and Colorama terminal output.

## Features

- Ten basic and advanced arithmetic operations
- Factory Design Pattern for arithmetic operation selection
- Memento Design Pattern for undo and redo functionality
- Observer Design Pattern for logging and automatic CSV saving
- Command Design Pattern for encapsulating calculator commands
- Decorator-based command registration and dynamic help generation
- Colorama for color-coded terminal output
- Calculation history management using pandas
- Manual CSV history saving and loading
- Environment-based configuration using python-dotenv
- Configurable maximum history size and result precision
- Input validation and exception handling
- Automated unit testing using pytest
- Code coverage measurement and enforcement using pytest-cov
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
├── .github/
├── .gitignore
├── requirements.txt
└── README.md
```

The application creates `logs/` and `history/` directories for generated log files and CSV calculation history.

The local `.env` configuration file is excluded from version control.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/islamnavid/midterm_is601.git
cd midterm_is601
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment.

On macOS or Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The main dependencies include:

- pandas
- python-dotenv
- colorama
- pytest
- pytest-cov

## Environment Configuration

The calculator uses environment variables to manage application settings.

Create a `.env` file in the project root directory with the following configuration:

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

### Configuration Settings

| Setting | Description |
|---|---|
| `CALCULATOR_LOG_DIR` | Directory for log files |
| `CALCULATOR_HISTORY_DIR` | Directory for history files |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of stored calculations |
| `CALCULATOR_AUTO_SAVE` | Enables or disables automatic history saving |
| `CALCULATOR_PRECISION` | Number of decimal places displayed |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum allowed input magnitude |
| `CALCULATOR_DEFAULT_ENCODING` | Default text encoding setting |
| `CALCULATOR_LOG_FILE` | Log filename |
| `CALCULATOR_HISTORY_FILE` | Automatic history CSV filename |

Configuration values are loaded using the `CalculatorConfig` class in `calculator_config.py`.

## Running the Calculator

Start the application:

```bash
python -m app.repl
```

The application displays:

```text
Welcome to the Calculator!
Type 'help' for available commands.
calculator>
```

Users can enter arithmetic operations or calculator commands directly into the REPL.

## Supported Arithmetic Operations

| Operation | Command | Example |
|---|---|---|
| Addition | `add` | `add 10 5` |
| Subtraction | `subtract` | `subtract 10 5` |
| Multiplication | `multiply` | `multiply 10 5` |
| Division | `divide` | `divide 10 5` |
| Exponentiation | `power` | `power 2 3` |
| Root | `root` | `root 16 2` |
| Modulus | `modulus` | `modulus 10 3` |
| Integer Division | `int_divide` | `int_divide 10 3` |
| Percentage | `percent` | `percent 20 100` |
| Absolute Difference | `abs_diff` | `abs_diff 10 5` |

### Example Calculations

With `CALCULATOR_PRECISION=2`:

```text
calculator> add 10 5
Result: 15.00

calculator> multiply 2.5 3
Result: 7.50

calculator> divide 10 3
Result: 3.33

calculator> power 2 3
Result: 8.00
```

Calculation precision affects displayed results without changing the underlying stored calculation values.

## REPL Commands

| Command | Description |
|---|---|
| `history` | Display previous calculations |
| `undo` | Undo the last history change |
| `redo` | Restore the last undone history change |
| `clear` | Clear calculation history |
| `save` | Save a manual history backup |
| `load` | Load a manual history backup |
| `help` | Display available commands |
| `exit` | Exit the application |

### Example History Management

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

### 1. Factory Design Pattern

**Implementation:** `app/operations.py`

The Factory Design Pattern selects the appropriate arithmetic operation based on the operation name.

This separates operation selection from calculation execution and makes the arithmetic system easier to maintain and extend.

### 2. Memento Design Pattern

**Implementation:** `app/calculator_memento.py` and `app/history.py`

The Memento Design Pattern preserves snapshots of calculation history.

It supports:

- Undoing calculations
- Redoing previously undone changes
- Restoring cleared history
- Undoing history loading operations

### 3. Observer Design Pattern

**Implementation:** `app/observers.py`

The Observer Design Pattern separates logging and automatic history persistence from the calculator's arithmetic logic.

The application includes:

- `LoggingObserver`: Records completed calculations
- `AutoSaveObserver`: Automatically saves calculation history to CSV

Observers are notified after calculations are completed.

### 4. Command Design Pattern

**Implementation:** `app/commands.py`

The Command Design Pattern encapsulates calculator actions into separate command classes.

Each command implements an `execute()` method.

Examples include:

- `HistoryCommand`
- `UndoCommand`
- `RedoCommand`
- `ClearCommand`
- `SaveCommand`
- `LoadCommand`
- `HelpCommand`
- `ExitCommand`

This separates command execution from the REPL interface.

### 5. Decorator-Based Command Registration

**Implementation:** `app/command_registry.py`

The Decorator Pattern is used to register calculator commands with descriptions.

Commands are registered using decorators such as:

```python
@registry.register("history", "Show calculation history")
```

The registry generates help information dynamically from registered commands.

This reduces the need to manually maintain separate command descriptions.

## Colorama Terminal Output

**Implementation:** `app/repl.py`

Colorama provides color-coded terminal messages to improve readability.

The application uses different colors to distinguish:

- Green: Successful calculations and operations
- Red: Errors and invalid commands
- Yellow: Warnings and informational messages
- Cyan: Welcome messages and history information

This is one of the project's optional enhancements.

## Calculation History and CSV Persistence

The calculator maintains a history of completed calculations.

History records contain operation names, operands, results, and timestamps.

The application uses pandas for CSV-based persistence.

### Automatic Saving

When `CALCULATOR_AUTO_SAVE=true`, the calculator automatically saves completed calculations to:

```text
history/calculation_history.csv
```

History changes performed through the REPL are also synchronized with the automatic history file.

### Manual Saving and Loading

The `save` command creates a separate backup:

```text
history/manual_history.csv
```

The `load` command restores calculations from this manual backup.

Keeping manual and automatic files separate prevents automatic clearing from overwriting a previously saved manual backup.

### Maximum History Size

The `CALCULATOR_MAX_HISTORY_SIZE` setting controls the number of calculations retained in history.

With the default value of 100, older calculations are removed when the limit is exceeded.

## Logging

The calculator uses Python's logging module and the Observer Design Pattern to record completed calculations.

By default, log messages are stored in:

```text
logs/calculator.log
```

Logging provides a record of completed arithmetic operations and their results.

## Input Validation and Error Handling

The application includes validation and exception handling for arithmetic operations and REPL commands.

Examples include:

- Invalid numeric input
- Division by zero
- Non-finite numeric input
- Inputs exceeding configured limits
- Missing CSV history files
- Invalid CSV history formats
- Unknown calculator commands

Error handling allows the calculator to continue running after recoverable input errors.

## Automated Testing

The project uses pytest for automated unit testing and pytest-cov for code coverage measurement.

Tests cover arithmetic operations, calculation execution, history management, undo/redo, configuration, observers, command registration, command execution, and REPL behavior.

### Run All Tests

```bash
python -m pytest -q
```

### Generate a Coverage Report

```bash
python -m pytest --cov=app --cov-report=term-missing
```

### Enforce Minimum 90% Coverage

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

### Latest Verified Test Results

**Local testing environment:** Python 3.14.7 on macOS

| Metric | Result |
|---|---|
| Total tests | 109 |
| Passed | 109 |
| Failed | 0 |
| Total code coverage | 98.48% |
| Required coverage | 90% |
| Coverage requirement | Passed |

### Coverage by Component

| Component | Coverage |
|---|---:|
| `calculation.py` | 100% |
| `calculator.py` | 100% |
| `calculator_config.py` | 92% |
| `calculator_memento.py` | 100% |
| `command_registry.py` | 100% |
| `commands.py` | 100% |
| `history.py` | 100% |
| `observers.py` | 100% |
| `operations.py` | 100% |
| `repl.py` | 94% |
| **Overall** | **98.48%** |

## Continuous Integration with GitHub Actions

The project uses GitHub Actions for automated testing.

The workflow is located at:

```text
.github/workflows/python-app.yml
```

The workflow runs when:

- Changes are pushed to `main`
- Pull requests target `main`
- The workflow is manually triggered

The workflow uses Python 3.11, installs project dependencies, runs pytest, and enforces the minimum 90% coverage requirement.

GitHub Actions helps verify that changes do not break existing functionality.

## Git Version Control

Git is used throughout development to track changes through incremental commits.

The development process includes separate commits for calculator functionality, design patterns, configuration, automated tests, REPL improvements, and documentation.

The `.gitignore` file excludes generated files, virtual environments, temporary data, and local environment configuration.

## GitHub Repository

https://github.com/islamnavid/midterm_is601

## Development Status

The Enhanced Calculator Command-Line Application implements the required calculator functionality, design patterns, history management, configuration, logging, CSV persistence, automated testing, and continuous integration.

All three optional enhancements have also been implemented:

1. Command Design Pattern
2. Decorator-based dynamic help
3. Colorama terminal output

The latest verified local test run completed with **109 passing tests and 98.48% code coverage**, exceeding the project's minimum coverage requirement.

Developed for the NJIT IS601 Midterm Project.