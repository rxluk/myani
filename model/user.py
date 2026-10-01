class User:
    def __init__(self, name, username, email, nickname, role_id, status, created_at, updated_at, id=None, salt=None, password_hash=None):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.nickname = nickname
        self.role_id = role_id
        self.status = status
        self.salt = salt
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nickname": self.nickname,
            "role_id": self.role_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
