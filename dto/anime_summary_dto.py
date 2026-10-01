class AnimeSummaryDTO:
    def __init__(self, anime, total_episodes):
        self.anime = anime
        self.total_episodes = total_episodes

    def to_dict(self):
        return {
            **self.anime.to_dict(),
            "total_episodes": self.total_episodes,
        }
