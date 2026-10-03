from service.exceptions import NotFoundError


class WatchedEpisodeService:
    def __init__(self, user_repository, anime_repository, watched_episode_repository):
        self._user_repository = user_repository
        self._anime_repository = anime_repository
        self._watched_episode_repository = watched_episode_repository

    def find_watched_animes(self, nickname, page, per_page):
        user = self._find_user(nickname)
        offset = (page - 1) * per_page
        animes = self._anime_repository.find_watched_by_user_id(user.id, per_page, offset)
        total = self._anime_repository.count_watched_by_user_id(user.id)
        return animes, total

    def find_watched_episodes(self, nickname, anime_id, page, per_page):
        user = self._find_user(nickname)
        if self._anime_repository.find_by_id(anime_id) is None:
            raise NotFoundError("Anime not found")
        offset = (page - 1) * per_page
        episodes = self._watched_episode_repository.find_by_user_and_anime(user.id, anime_id, per_page, offset)
        total = self._watched_episode_repository.count_by_user_and_anime(user.id, anime_id)
        return episodes, total

    def _find_user(self, nickname):
        user = self._user_repository.find_by_nickname(nickname)
        if user is None:
            raise NotFoundError("User not found")
        return user
