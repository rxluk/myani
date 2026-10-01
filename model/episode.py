class Episode:
    def __init__(self, name, description, number, anime_id, air_date=None, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.number = number
        self.air_date = air_date
        self.anime_id = anime_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "number": self.number,
            "air_date": self.air_date.isoformat() if self.air_date else None,
            "anime_id": self.anime_id,
        }
