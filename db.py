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
        script = """SELECT Artist.Name, COUNT(*) AS albums
                    FROM Artist, Album
                    WHERE Album.ArtistId = Artist.ArtistId
                    GROUP BY Artist.Name
                    ORDER BY albums DESC, Artist.Name;"""
        data = cursor.execute(script).fetchall()
        return data

    @staticmethod
    @functools.cache
    @get_cursor
    def get_tracks_count_by_duration(
            artist_id: int | None,
            album_id: int | None,
            duration_step: int,
            threshold: int,
            cursor: sqlite3.Cursor
    ) -> list[tuple[int, int]]:
        if artist_id is None and album_id is None:
            script = """SELECT Milliseconds/? AS duration_batch, COUNT(*) AS count
                        FROM Track
                        GROUP BY duration_batch
                        HAVING count > ?
                        ORDER BY duration_batch;"""
            parameters = [duration_step, threshold]
        elif album_id:
            script = """SELECT Milliseconds/? AS duration_batch, COUNT(*) AS count
                        FROM Track, Album
                        WHERE Album.AlbumId = Track.AlbumId AND Album.AlbumId = ?
                        GROUP BY duration_batch
                        HAVING count > ?
                        ORDER BY duration_batch;"""
            parameters = [duration_step, album_id, threshold]
        else:
            script = """SELECT Milliseconds/? AS duration_batch, COUNT(*) AS count
                        FROM Track, Album, Artist
                        WHERE Album.AlbumId = Track.AlbumId AND Artist.ArtistId = ? AND Artist.ArtistId = Album.ArtistId
                        GROUP BY duration_batch
                        HAVING count > ?
                        ORDER BY duration_batch"""
            parameters = [duration_step, artist_id, threshold]
        data = cursor.execute(script, parameters).fetchall()
        return data

    @staticmethod
    @functools.cache
    @get_cursor
    def get_artists(cursor: sqlite3.Cursor) -> list[tuple[str, int]]:
        script = """SELECT Name, ArtistId
                    From Artist
                    ORDER BY Name;"""
        data = cursor.execute(script).fetchall()
        return data

    @staticmethod
    @functools.cache
    @get_cursor
    def get_albums(artist_id: int, cursor: sqlite3.Cursor) -> list[tuple[str, int]]:
        if artist_id:
            script = """SELECT Title, AlbumId
                        FROM Album, Artist
                        WHERE Album.ArtistId = Artist.ArtistId AND Album.ArtistId = ?
                        ORDER BY Title;"""
            parameters = [artist_id]
        else:
            script = """SELECT Title, AlbumId
                        FROM Album
                        ORDER BY Title;"""
            parameters = []
        data = cursor.execute(script, parameters).fetchall()
        return data


if __name__ == "__main__":
    db = DB()
    db.recreate_db()
