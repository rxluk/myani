from model.user import User

USER_COLUMNS = "id, name, username, nickname, email, role_id, status, created_at, updated_at"


class UserRepository:
    def __init__(self, database):
        self._database = database

    def search(self, search_text, limit, offset):
        pattern = f"%{search_text}%"
        rows = self._database.fetch_all(
            f"SELECT {USER_COLUMNS} FROM users WHERE name ILIKE %s OR nickname ILIKE %s "
            "ORDER BY nickname LIMIT %s OFFSET %s",
            (pattern, pattern, limit, offset),
        )
        return [self._to_model(row) for row in rows]

    def count_search(self, search_text):
        pattern = f"%{search_text}%"
        row = self._database.fetch_one(
            "SELECT COUNT(*) AS total FROM users WHERE name ILIKE %s OR nickname ILIKE %s",
            (pattern, pattern),
        )
        return row["total"]

    def find_by_email_username_or_nickname(self, email, username, nickname):
        rows = self._database.fetch_all(
            f"SELECT {USER_COLUMNS} FROM users WHERE email = %s OR username = %s OR nickname = %s",
            (email, username, nickname),
        )
        return [self._to_model(row) for row in rows]

    def find_by_nickname(self, user_nickname):
        row = self._database.fetch_one(
            f"SELECT {USER_COLUMNS} FROM users WHERE nickname = %s",
            (user_nickname,),
        )
        return self._to_model(row) if row else None

    def find_by_id(self, user_id):
        row = self._database.fetch_one(
            f"SELECT {USER_COLUMNS} FROM users WHERE id = %s",
            (user_id,),
        )
        return self._to_model(row) if row else None

    def find_by_username(self, user_username):
        row = self._database.fetch_one(
            f"SELECT {USER_COLUMNS}, salt, password_hash FROM users WHERE username = %s",
            (user_username,),
        )
        return self._to_model(row) if row else None

    def find_by_email(self, user_email):
        row = self._database.fetch_one(
            f"SELECT {USER_COLUMNS}, salt, password_hash FROM users WHERE email = %s",
            (user_email,),
        )
        return self._to_model(row) if row else None

    def save(self, user):
        row, _ = self._database.execute(
            "INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash, status, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW()) RETURNING id",
            (
                user.name,
                user.username,
                user.nickname,
                user.email,
                user.role_id,
                user.salt,
                user.password_hash,
                user.status,
            ),
        )
        user.id = row["id"]
        return user

    def update(self, user):
        _, rowcount = self._database.execute(
            "UPDATE users SET name = %s, username = %s, nickname = %s, email = %s, role_id = %s, status = %s, "
            "updated_at = NOW() WHERE id = %s",
            (
                user.name,
                user.username,
                user.nickname,
                user.email,
                user.role_id,
                user.status,
                user.id,
            ),
        )
        return rowcount > 0

    def update_password(self, user_id, salt, password_hash):
        _, rowcount = self._database.execute(
            "UPDATE users SET salt = %s, password_hash = %s, updated_at = NOW() WHERE id = %s",
            (salt, password_hash, user_id),
        )
        return rowcount > 0

    def delete(self, user_id):
        _, rowcount = self._database.execute("DELETE FROM users WHERE id = %s", (user_id,))
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return User(
            id=row["id"],
            name=row["name"],
            username=row["username"],
            nickname=row["nickname"],
            email=row["email"],
            role_id=row["role_id"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            salt=row.get("salt"),
            password_hash=row.get("password_hash"),
        )
