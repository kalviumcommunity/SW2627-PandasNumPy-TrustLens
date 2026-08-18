import sqlite3

from src.database.validation import (
    get_row_count,
    get_table_names,
    table_exists,
)


def test_get_table_names():
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE seller_metrics (
            seller_id TEXT
        )
        """
    )

    tables = get_table_names(connection)

    assert "seller_metrics" in tables

    connection.close()


def test_table_exists():
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE seller_metrics (
            seller_id TEXT
        )
        """
    )

    assert table_exists(connection, "seller_metrics")
    assert not table_exists(connection, "unknown_table")

    connection.close()


def test_get_row_count():
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE seller_metrics (
            seller_id TEXT
        )
        """
    )

    connection.execute(
        """
        INSERT INTO seller_metrics (seller_id)
        VALUES ('seller_1')
        """
    )

    assert get_row_count(connection, "seller_metrics") == 1

    connection.close()