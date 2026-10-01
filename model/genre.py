class Genre:
    def __init__(self, name, description, id=None):
        self.name = name
        self.description = description
        self.id = id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            
        }
