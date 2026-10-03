from service.exceptions import NotFoundError


class AnimeService:
    def __init__(self, anime_repository, episode_repository):
        self._anime_repository = anime_repository
        self._episode_repository = episode_repository

    def search(self, title, page, per_page):
        offset = (page - 1) * per_page
        animes = self._anime_repository.search_by_title(title, per_page, offset)
        total = self._anime_repository.count_by_title(title)
        return animes, total

    def find_by_id(self, anime_id):
        anime = self._anime_repository.find_by_id(anime_id)
        if anime is None:
            raise NotFoundError("Anime not found")
        return anime

    def find_episodes(self, anime_id, page, per_page):
        self.find_by_id(anime_id)
        offset = (page - 1) * per_page
        episodes = self._episode_repository.find_by_anime_id(anime_id, per_page, offset)
        total = self._episode_repository.count_by_anime_id(anime_id)
        return episodes, total
