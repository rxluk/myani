class WatchedEpisodeDTO:
    def __init__(self, episode, status, score=None, watched_at=None):
        self.episode = episode
        self.status = status
        self.score = score
        self.watched_at = watched_at

    def to_dict(self):
        return {
            **self.episode.to_dict(),
            "status": self.status,
            "score": self.score,
            "watched_at": self.watched_at.isoformat() if self.watched_at else None,
        }
