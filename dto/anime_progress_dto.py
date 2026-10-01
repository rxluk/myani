class AnimeProgressDTO:
    def __init__(self, anime, watched_episodes, total_episodes):
        self.anime = anime
        self.watched_episodes = watched_episodes
        self.total_episodes = total_episodes

    def to_dict(self):
        return {
            **self.anime.to_dict(),
            "watched_episodes": self.watched_episodes,
            "total_episodes": self.total_episodes,
        }
