from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
from models.exceptions import ValidationError

class User:
    def __init__(self, data):
        self._id = str(data.get('_id', ObjectId()))
        self.username = data.get('username')
        self.password_hash = data.get('password_hash')
        self.failed_attempts = data.get('failed_attempts', 0)
        self.account_locked = data.get('account_locked', False)
        self.lock_time = data.get('lock_time')
        self.watchlist = data.get('watchlist', [])

        # Run validations
        self.validate()

    def validate(self):
        """Validate the required fields and data types for User."""
        if not self.username or not isinstance(self.username, str):
            raise ValidationError("Username is required and must be a string.")
        if not self.password_hash or not isinstance(self.password_hash, str):
            raise ValidationError("Password hash is required and must be a string.")
        if not isinstance(self.failed_attempts, int) or self.failed_attempts < 0:
            raise ValidationError("Failed attempts must be a non-negative integer.")
        if not isinstance(self.account_locked, bool):
            raise ValidationError("Account locked status must be a boolean.")
        if not isinstance(self.watchlist, list) or not all(isinstance(item, str) for item in self.watchlist):
            raise ValidationError("Watchlist must be a list of movie IDs as strings.")

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'watchlist': self.watchlist,
            'account_locked': self.account_locked,
            'failed_attempts': self.failed_attempts,
            'lock_time': self.lock_time
        }

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password).decode('utf-8')

    @staticmethod
    def check_password(hash, password):
        return check_password_hash(hash, password)
