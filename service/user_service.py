from model.user import User
from security.password import generate_salt, hash_password

DEFAULT_ROLE_NAME = "USER"
DEFAULT_STATUS = "ACTIVE"


class UserService:
    def __init__(self, user_repository, role_repository):
        self._user_repository = user_repository
        self._role_repository = role_repository

    def register(self, name, username, nickname, email, password):
        if not all([name, username, nickname, email, password]):
            raise ValueError("All fields are required")

        for existing_user in self._user_repository.find_by_email_username_or_nickname(email, username, nickname):
            if existing_user.email == email:
                raise ValueError("Email already registered")
            if existing_user.username == username:
                raise ValueError("Username already taken")
            if existing_user.nickname == nickname:
                raise ValueError("Nickname already taken")

        salt = generate_salt()
        user = User(
            name=name,
            username=username,
            nickname=nickname,
            email=email,
            role_id=self._role_repository.find_by_name(DEFAULT_ROLE_NAME).id,
            status=DEFAULT_STATUS,
            created_at=None,
            updated_at=None,
            salt=salt,
            password_hash=hash_password(password, salt),
        )
        return self._user_repository.save(user)

    def search(self, search_text, page, per_page):
        offset = (page - 1) * per_page
        users = self._user_repository.search(search_text, per_page, offset)
        total = self._user_repository.count_search(search_text)
        return users, total

    def find_by_nickname(self, nickname):
        return self._user_repository.find_by_nickname(nickname)
