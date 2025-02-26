import pytest
import main
import sqlite3


# Fixtures taken from Google AI and edited
@pytest.fixture
def connection():
    connection = sqlite3.connect('job_ads.db')
    yield connection


@pytest.fixture
def cursor(connection):
    cursor = connection.cursor()
    yield cursor


def test_SQL_Add(cursor):
    main.SQL_Add(['1', '2', '3', '4', '5', '6', '7', '8'], cursor)
    query = "SELECT * FROM personal_info ORDER BY rowid DESC LIMIT 1"
    result = list(cursor.execute(query))
    assert result == [(None, '1', '2', '3', '4', '5', '6', '7', '8')]
    main.SQL_Add(['doug', 'douglas', 'doug@gmail.com', '12345', '111222333', 'aa', 'aa', 'aa'], cursor)
    result = list(cursor.execute(query))
    assert result == [(None, 'doug', 'douglas', 'doug@gmail.com', '12345', '111222333', 'aa', 'aa', 'aa')]


def test_SQL_Search(cursor):
    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()
    assert list(main.SQL_Search('id', (0,), cursor)) == [('s-GCjOL5C9JmbOP8AAAAAA==',)]
    assert list(main.SQL_Search('title', (4,), cursor)) == [('Senior Software Development Engineer',)]
