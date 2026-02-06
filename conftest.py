import pytest
import abstarct_factory
from join_ import Column, Table
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


@pytest.fixture(scope="session")
def test_table() -> Table:
    test = Table('orders')

    test.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
    test.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))
    return test

@pytest.fixture(scope="session")
def test_value() -> dict:
    return ("тест", "тест2", "тест3")