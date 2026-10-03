from flask import request

DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 10


def get_pagination_params():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", DEFAULT_PER_PAGE, type=int)

    page = max(page, 1)
    per_page = min(max(per_page, 1), MAX_PER_PAGE)

    return page, per_page


def paginated_response(items, page, per_page, total):
    return {
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page,
    }
