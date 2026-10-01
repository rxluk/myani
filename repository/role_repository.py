from model.role import Role

ROLE_COLUMNS = "id, name"


class RoleRepository:
    def __init__(self, database):
        self._database = database

    def find_all(self):
        rows = self._database.fetch_all(f"SELECT {ROLE_COLUMNS} FROM roles")
        return [self._to_model(row) for row in rows]

    def find_by_id(self, role_id):
        row = self._database.fetch_one(
            f"SELECT {ROLE_COLUMNS} FROM roles WHERE id = %s",
            (role_id,),
        )
        return self._to_model(row) if row else None

    def find_by_name(self, role_name):
        row = self._database.fetch_one(
            f"SELECT {ROLE_COLUMNS} FROM roles WHERE name = %s",
            (role_name,),
        )
        return self._to_model(row) if row else None

    def save(self, role):
        row, _ = self._database.execute("INSERT INTO roles (name) VALUES (%s) RETURNING id", (role.name,))
        role.id = row["id"]
        return role

    def update(self, role):
        _, rowcount = self._database.execute(
            "UPDATE roles SET name = %s WHERE id = %s",
            (role.name, role.id),
        )
        return rowcount > 0

    def delete(self, role_id):
        _, rowcount = self._database.execute("DELETE FROM roles WHERE id = %s", (role_id,))
        return rowcount > 0

    def add_permission(self, role_id, permission_id):
        _, rowcount = self._database.execute(
            "INSERT INTO role_permission (role_id, permission_id) VALUES (%s, %s)",
            (role_id, permission_id),
        )
        return rowcount > 0

    def remove_permission(self, role_id, permission_id):
        _, rowcount = self._database.execute(
            "DELETE FROM role_permission WHERE role_id = %s AND permission_id = %s",
            (role_id, permission_id),
        )
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return Role(
            id=row["id"],
            name=row["name"],
        )
