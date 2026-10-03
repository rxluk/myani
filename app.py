from flask import Flask

from controller import anime_bp, user_bp

app = Flask(__name__)

app.register_blueprint(anime_bp, url_prefix="/animes")
app.register_blueprint(user_bp, url_prefix="/users")


@app.after_request
def allow_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


if __name__ == "__main__":
    app.run(debug=True)
