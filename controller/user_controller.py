from flask import Blueprint, request

from config.container import user_service
from controller.pagination import get_pagination_params, paginated_response

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
        return {"error": str(error)}, 409
    return user.to_dict(), 201


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
