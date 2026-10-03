from config.database_config import DB_CONNECTION_PARAMS, DatabaseConfig
from repository.anime_repository import AnimeRepository
from repository.episode_repository import EpisodeRepository
from repository.genre_repository import GenreRepository
from repository.permission_repository import PermissionRepository
from repository.role_repository import RoleRepository
from repository.user_repository import UserRepository
from repository.watched_episode_repository import WatchedEpisodeRepository
from service.user_service import UserService

database = DatabaseConfig(DB_CONNECTION_PARAMS)

anime_repository = AnimeRepository(database)
episode_repository = EpisodeRepository(database)
genre_repository = GenreRepository(database)
permission_repository = PermissionRepository(database)
role_repository = RoleRepository(database)
user_repository = UserRepository(database)
watched_episode_repository = WatchedEpisodeRepository(database)

user_service = UserService(user_repository, role_repository)
