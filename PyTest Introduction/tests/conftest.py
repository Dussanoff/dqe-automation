import os

import pytest
import pandas as pd

# Fixture to read the CSV file
@pytest.fixture(scope = "session")
def file():
    conftest_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(conftest_dir, "../src/data/data.csv")
    absolute_csv_path = os.path.abspath(csv_path)
    df = pd.read_csv(absolute_csv_path)
    return df


# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def schema(file):
    actual = list(file.columns)
    expected = ["id", "name", "age", "email"]
    return actual, expected


@pytest.fixture(scope = "session")
def players_data():
    return [(2, True)]

@pytest.fixture(scope = "session")
def list_of_dict(file):
    return file.to_dict(orient="records")


# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(config, items):
    for item in items:
        if not item.own_markers:
            item.add_marker("unmarked")
