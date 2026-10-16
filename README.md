# Enhanced Calculator Command-Line Application

## Project Overview

This project is an enhanced Python calculator developed for the **NJIT IS601 Midterm Project**.

The application provides an interactive command-line interface (REPL) for performing basic and advanced arithmetic calculations.

It demonstrates object-oriented programming, software design patterns, environment-based configuration, calculation history management, logging, CSV persistence, input validation, error handling, and automated testing.

The project also implements three optional enhancements:

1. Command Design Pattern
2. Decorator-based dynamic help generation
3. Colorama terminal output

## Features

- Ten basic and advanced arithmetic operations
- Factory Design Pattern for arithmetic operation selection
- Memento Design Pattern for undo and redo functionality
- Observer Design Pattern for logging and automatic CSV saving
- Command Design Pattern for calculator commands
- Decorator-based command registration
- Dynamic arithmetic operation discovery and help generation
- Colorama for color-coded terminal output
- Calculation history management using pandas
- Manual CSV history saving and loading
- Environment-based configuration using python-dotenv
- Configurable maximum history size and result precision
- Input validation with custom exceptions
- INFO, WARNING, and ERROR logging
- Automated unit testing using pytest
- Code coverage measurement using pytest-cov
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
│   ├── test_input_validators.py
│   ├── test_memento.py
│   ├── test_observer.py
│   ├── test_operations.py
│   └── test_repl.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The application creates directories for generated log files and CSV calculation history.

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

### 4. Configure Environment Variables

Copy the example configuration file:

On macOS or Linux:

```bash
cp .env.example .env
```

On Windows Command Prompt:

```cmd
copy .env.example .env
```

Review the configuration values and adjust them if needed.

## Environment Configuration

The calculator uses environment variables to manage application settings.

The configuration is loaded using the `CalculatorConfig` class in `app/calculator_config.py`.

An example configuration is:

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

Configuration settings allow application behavior to be modified without changing the Python source code.

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

The calculator supports ten arithmetic operations.

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
| `help` | Display available commands and operations |
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

The `OperationFactory` manages available operations and provides methods for retrieving and listing them.

Arithmetic operations are discovered dynamically rather than maintained through a hardcoded list in the REPL.

This makes the calculator easier to extend with additional operations.

### 2. Memento Design Pattern

**Implementation:** `app/calculator_memento.py` and `app/history.py`

The Memento Design Pattern preserves snapshots of calculation history.

It supports:

- Undoing calculations
- Redoing previously undone changes
- Restoring cleared history
- Undoing history loading operations

History changes create checkpoints so that previous states can be restored.

The implementation avoids unnecessary duplicate checkpoints during clear and load operations.

### 3. Observer Design Pattern

**Implementation:** `app/observers.py`

The Observer Design Pattern separates logging and automatic history persistence from arithmetic execution.

The application includes:

- `LoggingObserver`: Records completed calculations
- `AutoSaveObserver`: Automatically saves calculation history to CSV

Observers are notified after successful calculations.

The logging observer also provides methods for recording warnings and errors from the REPL.

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

Decorators register calculator commands with descriptions.

For example:

```python
@registry.register("history", "Show calculation history")
```

The registry generates help information dynamically from registered commands.

The help system also lists arithmetic operations available through `OperationFactory`.

This reduces the need to manually maintain command and operation descriptions.

## Colorama Terminal Output

**Implementation:** `app/repl.py`

Colorama provides color-coded terminal messages to improve readability.

The application uses:

- Green for successful calculations and command results
- Red for errors and invalid commands
- Cyan for welcome messages, help, and history information

This improves the interactive user experience.

## Calculation History and CSV Persistence

The calculator maintains a history of completed calculations.

History records contain operation names, operands, results, and timestamps.

The application uses pandas for CSV-based persistence.

### Automatic Saving

When `CALCULATOR_AUTO_SAVE=true`, the calculator automatically saves completed calculations to a configured CSV file.

For example:

```text
history/calculation_history.csv
```

### Manual Saving and Loading

The `save` command creates a separate history backup.

For example:

```text
history/manual_history.csv
```

The `load` command restores calculations from the manual backup. CSV data is validated for required columns, valid operations, finite numeric values, matching results, and valid timestamps before the current history is changed.

Keeping manual and automatic history files separate prevents automatic saving from overwriting a previously created manual backup.

### Maximum History Size

The `CALCULATOR_MAX_HISTORY_SIZE` setting controls the number of calculations retained in history.

With a configured limit of 100, older calculations are removed when the limit is exceeded.

## Logging

**Implementation:** `app/observers.py` and `app/repl.py`

The calculator uses Python's logging module to record calculation activity, warnings, and errors.

Log messages are written to a configured file.

For example:

```text
logs/calculator.log
```

Three logging levels are supported:

| Level | Purpose |
|---|---|
| `INFO` | Successful calculations |
| `WARNING` | Unknown commands and incorrect operand counts |
| `ERROR` | Invalid numeric input, division by zero, and command execution errors |

### Example Log Entries

```text
INFO - add: 10.0, 5.0 = 15.0
ERROR - divide: Cannot divide by zero.
WARNING - Invalid number of operands: add 10
WARNING - Unknown command: unknown
```

Log entries also include timestamps.

The logging observer uses a unique logger name for each instance to prevent accidental reuse of existing logger handlers.

## Input Validation and Error Handling

**Implementation:** `app/input_validators.py`, `app/exceptions.py`, and `app/calculator.py`

The calculator validates arithmetic inputs before executing calculations.

Validation includes:

- Checking numeric input types
- Rejecting Boolean values as numeric operands
- Rejecting non-finite values such as NaN and infinity
- Enforcing configured input magnitude limits
- Handling invalid arithmetic operations

The application defines custom exceptions:

- `CalculatorError`: Base calculator exception
- `ValidationError`: Invalid calculator input
- `OperationError`: Calculator operation errors

The REPL also handles recoverable errors such as:

- Invalid numeric input
- Division by zero
- Missing operands
- Missing CSV history files
- Invalid CSV history formats
- Unknown calculator commands

Errors are displayed to users without terminating the interactive calculator session.

Relevant warnings and errors are also recorded in the log file.

## Automated Testing

The project uses pytest for automated unit testing and pytest-cov for code coverage measurement.

Tests cover:

- Arithmetic operations
- Calculation execution
- Input validation and custom exceptions
- History management
- Undo and redo
- Configuration
- Observer behavior
- Command registration
- Dynamic help generation
- Command execution
- REPL functionality
- Logging and error handling
- CSV format validation and safe history loading

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
| Total tests | 197 |
| Passed | 197 |
| Failed | 0 |
| Total code coverage | 98.97% |
| Required coverage | 90% |
| Coverage requirement | Passed |

### Coverage by Component

| Component | Coverage |
|---|---:|
| `calculation.py` | 100% |
| `calculator.py` | 100% |
| `calculator_config.py` | 100% |
| `calculator_memento.py` | 100% |
| `command_registry.py` | 100% |
| `commands.py` | 100% |
| `exceptions.py` | 100% |
| `history.py` | 100% |
| `input_validators.py` | 100% |
| `logger.py` | 100% |
| `observers.py` | 100% |
| `operations.py` | 100% |
| `repl.py` | 93% |
| **Overall** | **98.97%** |

## Continuous Integration with GitHub Actions

The project uses GitHub Actions for automated testing.

The workflow is located at:

```text
.github/workflows/python-app.yml
```

The workflow is configured to run when:

- Changes are pushed to `main`
- Pull requests target `main`
- The workflow is manually triggered

The workflow uses Python 3.11, installs project dependencies, runs pytest, and enforces the minimum 90% coverage requirement.

The workflow for commit `80c1181` completed successfully on GitHub Actions (Python 3.11). GitHub Actions helps verify that changes do not break existing functionality.

## Git Version Control

Git is used throughout development to track changes through incremental commits.

The development process includes separate commits for calculator functionality, design patterns, configuration, automated tests, REPL improvements, and documentation.

The `.gitignore` file excludes generated files, virtual environments, temporary data, and local environment configuration.

## GitHub Repository

https://github.com/islamnavid/midterm_is601

## Development Status

The Enhanced Calculator Command-Line Application implements arithmetic operations, design patterns, history management, configuration, logging, CSV persistence, input validation, automated testing, and continuous integration.

All three optional enhancements have been implemented:

1. Command Design Pattern
2. Decorator-based dynamic help
3. Colorama terminal output

The latest verified local test run completed with **197 passing tests and 98.97% code coverage**, exceeding the project's minimum 90% coverage requirement.

Developed for the NJIT IS601 Midterm Project.
