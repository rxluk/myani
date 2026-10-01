from model.genre import Genre

GENRE_COLUMNS = "id, name, description"


class GenreRepository:
    def __init__(self, database):
        self._database = database

    def find_all(self):
        rows = self._database.fetch_all(f"SELECT {GENRE_COLUMNS} FROM genres ORDER BY name")
        return [self._to_model(row) for row in rows]

    def find_by_id(self, genre_id):
        row = self._database.fetch_one(
            f"SELECT {GENRE_COLUMNS} FROM genres WHERE id = %s",
            (genre_id,),
        )
        return self._to_model(row) if row else None

    def find_by_name(self, genre_name):
        row = self._database.fetch_one(
            f"SELECT {GENRE_COLUMNS} FROM genres WHERE name = %s",
            (genre_name,),
        )
        return self._to_model(row) if row else None

    def save(self, genre):
        row, _ = self._database.execute(
            "INSERT INTO genres (name, description) VALUES (%s, %s) RETURNING id",
            (genre.name, genre.description),
        )
        genre.id = row["id"]
        return genre

    def update(self, genre):
        _, rowcount = self._database.execute(
            "UPDATE genres SET name = %s, description = %s WHERE id = %s",
            (genre.name, genre.description, genre.id),
        )
        return rowcount > 0

    def delete(self, genre_id):
        _, rowcount = self._database.execute("DELETE FROM genres WHERE id = %s", (genre_id,))
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return Genre(
            id=row["id"],
            name=row["name"],
            description=row["description"],
        )
