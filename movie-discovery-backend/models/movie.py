from bson.objectid import ObjectId
from models.exceptions import ValidationError

class Movie:
    def __init__(self, data):
        # Required fields with validation
        self._id = str(data.get('_id', ObjectId()))
        self.title = data.get('title')
        self.year = data.get('year')
        self.rating = data.get('rating', 0.0)  # Default rating to 0.0 if not provided
        self.duration = data.get('runtime')
        self.genres = data.get('genres', [])
        self.director = data.get('director')
        self.cast = data.get('cast', [])
        self.description = data.get('description', "")

        # Run validations
        self.validate()

    def validate(self):
        """Validate the required fields and data types for Movie."""
        if not self.title or not isinstance(self.title, str):
            raise ValidationError("Movie title is required and must be a string.")
        if not isinstance(self.year, int) or self.year < 1800 or self.year > 2100:
            raise ValidationError("Movie year must be a valid integer between 1800 and 2100.")
        if not isinstance(self.genres, list) or not all(isinstance(genre, str) for genre in self.genres):
            raise ValidationError("Genres must be a list of strings.")
        if self.rating is not None and (not isinstance(self.rating, (int, float)) or self.rating < 0 or self.rating > 10):
            raise ValidationError("Rating must be a number between 0 and 10.")
        if self.duration is not None and (not isinstance(self.duration, int) or self.duration <= 0):
            raise ValidationError("Runtime must be a positive integer.")

    def to_dict(self):
        return {
            '_id': str(self._id),
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'runtime': self.duration,
            'genres': self.genres,
            'director': self.director,
            'cast': self.cast,
            'description': self.description
        }
