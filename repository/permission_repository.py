from model.permission import Permission

PERMISSION_COLUMNS = "id, name"


class PermissionRepository:
    def __init__(self, database):
        self._database = database

    def find_all(self):
        rows = self._database.fetch_all(f"SELECT {PERMISSION_COLUMNS} FROM permissions")
        return [self._to_model(row) for row in rows]

    def find_by_role_id(self, role_id):
        rows = self._database.fetch_all(
            "SELECT p.id, p.name FROM permissions p "
            "JOIN role_permission rp ON rp.permission_id = p.id "
            "WHERE rp.role_id = %s",
            (role_id,),
        )
        return [self._to_model(row) for row in rows]

    def find_by_id(self, permission_id):
        row = self._database.fetch_one(
            f"SELECT {PERMISSION_COLUMNS} FROM permissions WHERE id = %s",
            (permission_id,),
        )
        return self._to_model(row) if row else None

    def find_by_name(self, permission_name):
        row = self._database.fetch_one(
            f"SELECT {PERMISSION_COLUMNS} FROM permissions WHERE name = %s",
            (permission_name,),
        )
        return self._to_model(row) if row else None

    def save(self, permission):
        row, _ = self._database.execute("INSERT INTO permissions (name) VALUES (%s) RETURNING id", (permission.name,))
        permission.id = row["id"]
        return permission

    def update(self, permission):
        _, rowcount = self._database.execute(
            "UPDATE permissions SET name = %s WHERE id = %s",
            (permission.name, permission.id),
        )
        return rowcount > 0

    def delete(self, permission_id):
        _, rowcount = self._database.execute("DELETE FROM permissions WHERE id = %s", (permission_id,))
        return rowcount > 0

    @staticmethod
    def _to_model(row):
        return Permission(
            id=row["id"],
            name=row["name"],
        )
