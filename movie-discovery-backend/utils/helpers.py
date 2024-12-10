from bson import ObjectId
from flask import jsonify

def is_valid_object_id(value):
    """
    Validate if the provided value is a valid MongoDB ObjectId.
    Returns an ObjectId instance if valid, otherwise None.
    """
    try:
        return ObjectId(value)
    except (TypeError, ValueError):
        return None

def success_response(data, status_code=200):
    def convert_object_id(obj):
        if isinstance(obj, dict):
            return {k: convert_object_id(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_object_id(i) for i in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    return jsonify(convert_object_id(data)), status_code


def error_response(message, status_code=400):
    """Returns a JSON response for errors."""
    return jsonify({"error": message}), status_code

from extensions import mongo
from bson.objectid import ObjectId

def get_user_from_token(token):
    """
    Retrieves the user associated with the given Bearer token.
    
    Parameters:
        token (str): The token to validate and use for user lookup.
    
    Returns:
        dict: User data if token is valid and user exists, otherwise None.
    """
    try:
        user = mongo.cx.movies_db.users.find_one({"token": token})
        return user if user and user.get("token") == token else None
    except Exception as e:
        print(f"Error retrieving user by token: {e}")
        return None