class RolePermission:
    def __init__(self, role_id, permission_id):
        self.role_id = role_id
        self.permission_id = permission_id

    def to_dict(self):
        return {
            "role_id": self.role_id,
            "permission_id": self.permission_id,
        }
