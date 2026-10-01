class Anime:
    def __init__(self, title, cover_url, is_finished, title_english=None, episode_duration=None, id=None):
        self.id = id
        self.title = title
        self.title_english = title_english
        self.cover_url = cover_url
        self.is_finished = is_finished
        self.episode_duration = episode_duration

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "title_english": self.title_english,
            "cover_url": self.cover_url,
            "is_finished": self.is_finished,
            "episode_duration": self.episode_duration,
        }
