# utils/auth.py

from functools import wraps
from flask import request, jsonify
from utils.helpers import get_user_from_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'message': 'Token is missing or invalid'}), 401

        token = auth_header.split(" ")[1]
        user_data = get_user_from_token(token)
        
        if not user_data:
            return jsonify({'message': 'Token is invalid or user not found'}), 401

        request.user = user_data  # Attach user data to the request context
        return f(*args, **kwargs)
    return decorated

def is_admin():
    """
    Checks if the current user has admin privileges.
    """
    user_data = getattr(request, 'user', None)
    return user_data and user_data.get("is_admin", False)  # Checks if is_admin is True
