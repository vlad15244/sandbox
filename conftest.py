import pytest
import abstarct_factory
import pytest

@pytest.fixture(scope="session")
def db_localhost() -> str:
    return "localhost"

@pytest.fixture(scope="session")
def db_user() -> str:
    return "root"

@pytest.fixture(scope="session")
def db_pwd() -> str:
    return "1234"

@pytest.fixture(scope="session")
def insert_values() -> dict:
    return ("первый", "второй",)
