import pandas as pd

from app.calculator import Calculator
from app.observers import AutoSaveObserver


def test_auto_save_observer(tmp_path):
    file_path = tmp_path / "calculation_history.csv"

    calculator = Calculator()
    observer = AutoSaveObserver(
        calculator.history,
        file_path=str(file_path)
    )
    calculator.add_observer(observer)

    calculator.calculate("add", 10, 5)
    calculator.calculate("multiply", 4, 5)

    assert file_path.exists()

    data = pd.read_csv(file_path)

    assert len(data) == 2
    assert data["result"].tolist() == [15, 20]
    assert data["operation"].tolist() == ["add", "multiply"]