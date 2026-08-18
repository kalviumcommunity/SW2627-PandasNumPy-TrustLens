from src.database.connection import get_database_path


def test_database_path():
    path = get_database_path()

    assert path.name == "trustlens.db"
    assert path.parent.name == "database"