from model.episode import Episode

EPISODE_COLUMNS = "id, name, description, number, air_date, anime_id"


class EpisodeRepository:
    def __init__(self, database):
        self._database = database

    def find_by_anime_id(self, anime_id, limit, offset):
        rows = self._database.fetch_all(
            f"SELECT {EPISODE_COLUMNS} FROM episodes WHERE anime_id = %s ORDER BY number LIMIT %s OFFSET %s",
            (anime_id, limit, offset),
        )
        return [self._to_model(row) for row in rows]

    def count_by_anime_id(self, anime_id):
        row = self._database.fetch_one(
            "SELECT COUNT(*) AS total FROM episodes WHERE anime_id = %s",
            (anime_id,),
        )
        return row["total"]

    def find_by_id(self, episode_id):
        row = self._database.fetch_one(
            f"SELECT {EPISODE_COLUMNS} FROM episodes WHERE id = %s",
            (episode_id,),
        )
        return self._to_model(row) if row else None

    def save(self, episode):
        row, _ = self._database.execute(
            "INSERT INTO episodes (name, description, number, air_date, anime_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (episode.name, episode.description, episode.number, episode.air_date, episode.anime_id),
        )
        episode.id = row["id"]
        return episode

    def update(self, episode):
        _, rowcount = self._database.execute(
            "UPDATE episodes SET name = %s, description = %s, number = %s, air_date = %s, anime_id = %s "
            "WHERE id = %s",
            (episode.name, episode.description, episode.number, episode.air_date, episode.anime_id, episode.id),
        )
        return rowcount > 0

    def delete(self, episode_id):
        _, rowcount = self._database.execute("DELETE FROM episodes WHERE id = %s", (episode_id,))
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return Episode(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            number=row["number"],
            air_date=row["air_date"],
            anime_id=row["anime_id"],
        )
