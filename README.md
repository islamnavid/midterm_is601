# Enhanced Calculator Command-Line Application

## Project Overview

This project is an enhanced Python calculator developed for the IS601 Midterm Project.

The application provides an interactive command-line interface (REPL) for performing arithmetic calculations. It incorporates design patterns, calculation history, undo/redo functionality, logging, CSV persistence, and automated testing.

## Features

- Basic and advanced arithmetic operations
- Factory Design Pattern for selecting arithmetic operations
- Memento Design Pattern for undo and redo functionality
- Observer Design Pattern for logging and automatic CSV saving
- Calculation history management using pandas
- Interactive command-line interface (REPL)
- Environment-based configuration
- Input validation and error handling
- Automated unit testing with pytest
- Test coverage reporting using pytest-cov

## Project Structure

```text
midterm_is601/
├── app/
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
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
│   ├── test_history.py
│   ├── test_memento.py
│   ├── test_observer.py
│   ├── test_operations.py
│   └── test_repl.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/islamnavid/midterm_is601.git
cd midterm_is601
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Calculator

Start the interactive calculator:

```bash
python -m app.repl
```

### Example Commands

```text
calculator> add 10 5
Result: 15.0

calculator> multiply 4 5
Result: 20.0

calculator> history
add: 10.0, 5.0 = 15.0
multiply: 4.0, 5.0 = 20.0

calculator> undo
Undo successful.

calculator> redo
Redo successful.

calculator> clear
History cleared.

calculator> exit
Goodbye!
```

The calculator also supports additional operations, including power, root, modulus, integer division, percentage, and absolute difference.

## Design Patterns

### Factory Design Pattern

The Factory Design Pattern is implemented in `operations.py` to select the appropriate arithmetic operation based on the user's input.

### Memento Design Pattern

The Memento Design Pattern enables users to undo and redo changes to calculation history by restoring previously saved states.

### Observer Design Pattern

The Observer Design Pattern is used to log completed calculations and automatically save calculation history to CSV files.

## Calculation History

The application maintains calculation history using pandas and supports CSV-based persistence.

Users can view their calculation history, clear previous calculations, and undo or redo changes.

## Logging

The calculator records completed operations through the logging observer. Log messages are written to `calculator.log`.

## Automated Testing

The project uses pytest for automated testing.

Run all tests:

```bash
python -m pytest -q
```

Generate a coverage report:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

### Latest Test Results

- 83 automated tests passed
- 96% total code coverage
- Arithmetic operations, calculation history, design patterns, and REPL functionality tested

## GitHub Repository

https://github.com/islamnavid/midterm_is601

## Development Status

