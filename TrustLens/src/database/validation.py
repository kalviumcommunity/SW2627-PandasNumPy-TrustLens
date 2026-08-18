"""Database validation utilities for TrustLens."""

from __future__ import annotations

import sqlite3


def get_table_names(connection: sqlite3.Connection) -> list[str]:
    """Return all user-created table names in the database."""

    cursor = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )

    return [row[0] for row in cursor.fetchall()]


def table_exists(
    connection: sqlite3.Connection,
    table_name: str,
) -> bool:
    """Check whether a table exists."""

    return table_name in get_table_names(connection)


def get_row_count(
    connection: sqlite3.Connection,
    table_name: str,
) -> int:
    """Return the number of rows in a table."""

    if not table_exists(connection, table_name):
        raise ValueError(
            f"Table '{table_name}' does not exist."
        )

    cursor = connection.execute(
        f'SELECT COUNT(*) FROM "{table_name}"'
    )

    return int(cursor.fetchone()[0])