from model.anime import Anime

ANIME_COLUMNS = "id, title, title_english, cover_url, is_finished, episode_duration"
TITLE_SEARCH_FILTER = "title ILIKE %s OR title_english ILIKE %s"


class AnimeRepository:
    def __init__(self, database):
        self._database = database

    def search_by_title(self, anime_title, limit, offset):
        pattern = f"%{anime_title}%"
        rows = self._database.fetch_all(
            f"SELECT {ANIME_COLUMNS} FROM animes WHERE {TITLE_SEARCH_FILTER} ORDER BY title LIMIT %s OFFSET %s",
            (pattern, pattern, limit, offset),
        )
        return [self._to_model(row) for row in rows]

    def count_by_title(self, anime_title):
        pattern = f"%{anime_title}%"
        row = self._database.fetch_one(
            f"SELECT COUNT(*) AS total FROM animes WHERE {TITLE_SEARCH_FILTER}",
            (pattern, pattern),
        )
        return row["total"]

    def find_by_id(self, anime_id):
        row = self._database.fetch_one(
            f"SELECT {ANIME_COLUMNS} FROM animes WHERE id = %s",
            (anime_id,),
        )
        return self._to_model(row) if row else None

    def save(self, anime):
        row, _ = self._database.execute(
            "INSERT INTO animes (title, title_english, cover_url, is_finished, episode_duration) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (anime.title, anime.title_english, anime.cover_url, anime.is_finished, anime.episode_duration),
        )
        anime.id = row["id"]
        return anime

    def update(self, anime):
        _, rowcount = self._database.execute(
            "UPDATE animes SET title = %s, title_english = %s, cover_url = %s, is_finished = %s, "
            "episode_duration = %s WHERE id = %s",
            (
                anime.title,
                anime.title_english,
                anime.cover_url,
                anime.is_finished,
                anime.episode_duration,
                anime.id,
            ),
        )
        return rowcount > 0

    def delete(self, anime_id):
        _, rowcount = self._database.execute("DELETE FROM animes WHERE id = %s", (anime_id,))
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return Anime(
            id=row["id"],
            title=row["title"],
            title_english=row["title_english"],
            cover_url=row["cover_url"],
            is_finished=bool(row["is_finished"]),
            episode_duration=row["episode_duration"],
        )
