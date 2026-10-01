from flask import Flask

from config.database_config import DB_CONNECTION_PARAMS, DatabaseConfig
from repository.anime_repository import AnimeRepository

app = Flask(__name__)

database = DatabaseConfig(DB_CONNECTION_PARAMS)


if __name__ == "__main__":
    app.run(debug=True)
