class AnimeGenre:
    def __init__(self, anime, genre):
        self.anime = anime
        self.genre = genre

    def to_dict(self):
        return {
            "anime": self.anime,
            "genre": self.genre,
        }
