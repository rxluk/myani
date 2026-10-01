class WatchedEpisode:
    def __init__(self, user_id, episode_id, status, watched_at=None, score=None, id=None):
        self.user_id = user_id
        self.episode_id = episode_id
        self.status = status
        self.watched_at = watched_at
        self.score = score
        self.id = id

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "episode_id": self.episode_id,
            "status": self.status,
            "score": self.score,
            "watched_at": self.watched_at.isoformat() if self.watched_at else None,
        }
