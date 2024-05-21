import sqlite3


script_path = "Chinook_Sqlite.sql"
db_path = "db.sqlite3"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def recreate_db() -> None:
    connection = get_connection()
    with open(script_path, 'r') as file:
        script = "".join(file.readlines())
        connection.executescript(script)


if __name__ == "__main__":
    recreate_db()
