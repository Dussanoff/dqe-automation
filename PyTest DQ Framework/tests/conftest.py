import os

import pytest
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.data_quality.data_quality_validation_library import DataQualityLibrary
from src.connectors.file_system.parquet_reader import ParquetReader


def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost", help="Database host")
    parser.addoption("--db_port", action="store", default="5434", help="Database port")
    parser.addoption("--db_name", action="store", default="mydatabase", help="Database name")
    parser.addoption("--db_user", action="store", #default=os.environ.get("POSTGRES_SECRET_USR")
                     help="Database user")
    parser.addoption("--db_password", action="store", #default=os.environ.get("POSTGRES_SECRET_PSW")
                     help="Database password")


def pytest_configure(config):
    """
    Validates that all required command-line options are provided.
    """
    required_options = [
        "--db_user", "--db_password"
    ]
    for option in required_options:
        if not config.getoption(option):
            pytest.fail(f"Missing required option: {option}")


@pytest.fixture(scope="session")
def db_connection(request):
    host = request.config.getoption("--db_host")
    port = int(request.config.getoption("--db_port"))
    database = request.config.getoption("--db_name")
    user = request.config.getoption("--db_user")
    password = request.config.getoption("--db_password")
    try:
        with PostgresConnectorContextManager(host, port, database, user, password) as db_connector:
            yield db_connector
    except Exception as e:
        pytest.fail(f"Failed to initialize PostgresConnectorContextManager: {e}")


@pytest.fixture(scope="session")
def parquet_reader():
    try:
        reader = ParquetReader()
        yield reader
    except Exception as e:
        pytest.fail(f"Failed to initialize ParquetReader: {e}")
    finally:
        del reader


@pytest.fixture(scope='session')
def data_quality_library():
    try:
        data_quality_library = DataQualityLibrary()
        yield data_quality_library
    except Exception as e:
        pytest.fail(f"Failed to initialize DataQualityLibrary: {e}")
    finally:
        del data_quality_library

