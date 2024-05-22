import functools
import sqlite3
from typing import Any, Callable


script_path = "Chinook_Sqlite.sql"
db_path = "db.sqlite3"


class DB:
    @staticmethod
    def get_cursor(function: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            kwargs["cursor"] = cursor
            result = function(*args, **kwargs)
            connection.close()
            return result

        return wrapper

    @staticmethod
    @get_cursor
    def recreate_db(cursor: sqlite3.Cursor) -> None:
        with open(script_path, 'r') as file:
            script = "".join(file.readlines())
            cursor.executescript(script)

    @staticmethod
    @functools.cache
    @get_cursor
    def get_artists_album_count(cursor: sqlite3.Cursor) -> list[tuple[str, int]]:
        script = """SELECT Artist.Name, COUNT(*) as albums
                    FROM Artist, Album
                    WHERE Album.ArtistId = Artist.ArtistId
                    GROUP BY Artist.Name
                    ORDER BY albums DESC, Artist.Name;"""
        data = cursor.execute(script).fetchall()
        return data

    @staticmethod
    @functools.cache
    @get_cursor
    def get_tracks_count_by_duration(duration_step: int, threshold: int, cursor: sqlite3.Cursor) -> list[tuple[int, int]]:
        script = """SELECT Milliseconds/? as duration_batch, COUNT(*) as count
                    FROM Track
                    GROUP BY duration_batch
                    HAVING count > ?
                    ORDER BY duration_batch;"""
        data = cursor.execute(script, [duration_step, threshold]).fetchall()
        return data


if __name__ == "__main__":
    db = DB()
    db.recreate_db()
