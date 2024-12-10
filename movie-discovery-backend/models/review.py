from bson.objectid import ObjectId
from datetime import datetime
from models.exceptions import ValidationError

class Review:
    def __init__(self, data):
        self._id = str(data.get('_id', ObjectId()))
        self.movie_id = str(data.get('movie_id'))
        self.user_id = str(data.get('user_id'))
        self.rating = data.get('rating')
        self.review = data.get('review', "")
        self.timestamp = data.get('timestamp', datetime.utcnow())

        # Run validations
        self.validate()

    def validate(self):
        """Validate the required fields and data types for Review."""
        if not ObjectId.is_valid(self.movie_id):
            raise ValidationError("movie_id must be a valid ObjectId string.")
        if not ObjectId.is_valid(self.user_id):
            raise ValidationError("user_id must be a valid ObjectId string.")
        if not isinstance(self.rating, (int, float)) or self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be a number between 0 and 5.")
        if not isinstance(self.review, str):
            raise ValidationError("Review must be a string.")
        if not isinstance(self.timestamp, datetime):
            raise ValidationError("Timestamp must be a datetime object.")

    def to_dict(self):
        return {
            '_id': str(self._id),  # Convert ObjectId to string
            'movie_id': self.movie_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'review': self.review,
            'timestamp': self.timestamp.isoformat()
        }

