from dto.watched_episode_dto import WatchedEpisodeDTO
from model.episode import Episode
from model.watched_episode import WatchedEpisode

WATCHED_EPISODE_COLUMNS = "id, user_id, episode_id, status, score, watched_at"


class WatchedEpisodeRepository:
    def __init__(self, database):
        self._database = database

    def find_by_user_id(self, user_id):
        rows = self._database.fetch_all(
            f"SELECT {WATCHED_EPISODE_COLUMNS} FROM watched_episode WHERE user_id = %s ORDER BY watched_at DESC",
            (user_id,),
        )
        return [self._to_model(row) for row in rows]

    def find_by_id(self, watched_episode_id):
        row = self._database.fetch_one(
            f"SELECT {WATCHED_EPISODE_COLUMNS} FROM watched_episode WHERE id = %s",
            (watched_episode_id,),
        )
        return self._to_model(row) if row else None

    def find_by_user_and_anime(self, user_id, anime_id, limit, offset):
        rows = self._database.fetch_all(
            "SELECT e.id, e.name, e.description, e.number, e.air_date, e.anime_id, w.status, w.score, w.watched_at "
            "FROM watched_episode w "
            "JOIN episodes e ON e.id = w.episode_id "
            "WHERE w.user_id = %s AND e.anime_id = %s "
            "ORDER BY e.number "
            "LIMIT %s OFFSET %s",
            (user_id, anime_id, limit, offset),
        )
        return [self._to_dto(row) for row in rows]

    def count_by_user_and_anime(self, user_id, anime_id):
        row = self._database.fetch_one(
            "SELECT COUNT(*) AS total "
            "FROM watched_episode w "
            "JOIN episodes e ON e.id = w.episode_id "
            "WHERE w.user_id = %s AND e.anime_id = %s",
            (user_id, anime_id),
        )
        return row["total"]

    def find_by_user_and_episode(self, user_id, episode_id):
        row = self._database.fetch_one(
            f"SELECT {WATCHED_EPISODE_COLUMNS} FROM watched_episode WHERE user_id = %s AND episode_id = %s",
            (user_id, episode_id),
        )
        return self._to_model(row) if row else None

    def save(self, watched_episode):
        row, _ = self._database.execute(
            "INSERT INTO watched_episode (user_id, episode_id, status, score, watched_at) "
            "VALUES (%s, %s, %s, %s, COALESCE(%s, NOW())) RETURNING id",
            (
                watched_episode.user_id,
                watched_episode.episode_id,
                watched_episode.status,
                watched_episode.score,
                watched_episode.watched_at,
            ),
        )
        watched_episode.id = row["id"]
        return watched_episode

    def update(self, watched_episode):
        _, rowcount = self._database.execute(
            "UPDATE watched_episode SET status = %s, score = %s, watched_at = %s WHERE id = %s",
            (
                watched_episode.status,
                watched_episode.score,
                watched_episode.watched_at,
                watched_episode.id,
            ),
        )
        return rowcount > 0

    def delete(self, watched_episode_id):
        _, rowcount = self._database.execute("DELETE FROM watched_episode WHERE id = %s", (watched_episode_id,))
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return WatchedEpisode(
            id=row["id"],
            user_id=row["user_id"],
            episode_id=row["episode_id"],
            status=row["status"],
            score=row["score"],
            watched_at=row["watched_at"],
        )

    @staticmethod
    def _to_dto(row):
        episode = Episode(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            number=row["number"],
            air_date=row["air_date"],
            anime_id=row["anime_id"],
        )
        return WatchedEpisodeDTO(
            episode=episode,
            status=row["status"],
            score=row["score"],
            watched_at=row["watched_at"],
        )
