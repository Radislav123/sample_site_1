import functools
import sqlite3


script_path = "Chinook_Sqlite.sql"
db_path = "db.sqlite3"


class DB:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    @classmethod
    def recreate_db(cls) -> None:
        with open(script_path, 'r') as file:
            script = "".join(file.readlines())
            cls.connection.executescript(script)

    @classmethod
    @functools.cache
    def get_artists_album_count(cls) -> list[tuple[str, int]]:
        script = """SELECT Artist.Name, COUNT(*) as albums
                    FROM Artist, Album
                    WHERE Album.ArtistId = Artist.ArtistId
                    GROUP BY Artist.Name
                    ORDER BY albums DESC, Artist.Name;"""
        data = cls.cursor.execute(script).fetchall()
        return data


if __name__ == "__main__":
    db = DB()
    # db.recreate_db()
    db.get_artists_album_count()
