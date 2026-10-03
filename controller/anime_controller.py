from flask import Blueprint

from config.container import anime_service
from controller.pagination import get_pagination_params, paginated_response
from service.exceptions import NotFoundError

anime_bp = Blueprint("anime", __name__)


@anime_bp.route("/search/<string:title>", methods=["GET"])
def search(title):
    page, per_page = get_pagination_params()
    animes, total = anime_service.search(title, page, per_page)
    return paginated_response([anime.to_dict() for anime in animes], page, per_page, total)


@anime_bp.route("/<int:anime_id>", methods=["GET"])
def find_by_id(anime_id):
    try:
        anime = anime_service.find_by_id(anime_id)
    except NotFoundError as error:
        return {"error": str(error)}, 404
    return anime.to_dict()


@anime_bp.route("/<int:anime_id>/episodes", methods=["GET"])
def find_episodes(anime_id):
    page, per_page = get_pagination_params()
    try:
        episodes, total = anime_service.find_episodes(anime_id, page, per_page)
    except NotFoundError as error:
        return {"error": str(error)}, 404
    return paginated_response([episode.to_dict() for episode in episodes], page, per_page, total)
