from flask import Blueprint, request

from config.container import user_service, watched_episode_service
from controller.pagination import get_pagination_params, paginated_response
from service.exceptions import ConflictError, NotFoundError, UnauthorizedError

user_bp = Blueprint("user", __name__)


@user_bp.route("", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    try:
        user = user_service.register(
            name=data.get("name"),
            username=data.get("username"),
            nickname=data.get("nickname"),
            email=data.get("email"),
            password=data.get("password"),
        )
    except ValueError as error:
        return {"error": str(error)}, 400
    except ConflictError as error:
        return {"error": str(error)}, 409
    return user.to_dict(), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    try:
        user = user_service.login(data.get("username"), data.get("password"))
    except ValueError as error:
        return {"error": str(error)}, 400
    except UnauthorizedError as error:
        return {"error": str(error)}, 401
    return user.to_dict()


@user_bp.route("/search/<string:search_text>", methods=["GET"])
def search(search_text):
    page, per_page = get_pagination_params()
    users, total = user_service.search(search_text, page, per_page)
    return paginated_response([user.to_dict() for user in users], page, per_page, total)


@user_bp.route("/<string:nickname>", methods=["GET"])
def find_by_nickname(nickname):
    user = user_service.find_by_nickname(nickname)
    if user is None:
        return {"error": "User not found"}, 404
    return user.to_dict()


@user_bp.route("/<string:nickname>/animes", methods=["GET"])
def find_watched_animes(nickname):
    page, per_page = get_pagination_params()
    try:
        animes, total = watched_episode_service.find_watched_animes(nickname, page, per_page)
    except NotFoundError as error:
        return {"error": str(error)}, 404
    return paginated_response([anime.to_dict() for anime in animes], page, per_page, total)


@user_bp.route("/<string:nickname>/animes/<int:anime_id>/episodes", methods=["GET"])
def find_watched_episodes(nickname, anime_id):
    page, per_page = get_pagination_params()
    try:
        episodes, total = watched_episode_service.find_watched_episodes(nickname, anime_id, page, per_page)
    except NotFoundError as error:
        return {"error": str(error)}, 404
    return paginated_response([episode.to_dict() for episode in episodes], page, per_page, total)
