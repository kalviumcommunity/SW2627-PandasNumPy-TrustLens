"""SQLite database connection utilities for TrustLens."""

from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "data" / "database"
DATABASE_PATH = DATABASE_DIR / "trustlens.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a connection to the TrustLens SQLite database."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def get_database_path() -> Path:
    """Return the path to the TrustLens SQLite database."""
    return DATABASE_PATH