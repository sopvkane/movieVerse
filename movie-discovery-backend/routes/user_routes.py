import uuid
from flask import Blueprint, request, jsonify
from utils.helpers import success_response, error_response, get_user_from_token
from services.user_service import (
    register_new_user, validate_user_credentials, get_user_profile,
    add_movie_to_watchlist, remove_movie_from_watchlist, get_user_watchlist
)
from extensions import mongo
from utils.auth import token_required, is_admin

user_bp = Blueprint('user_bp', __name__)

def generate_token():
    """Generate a unique token for the user session."""
    return str(uuid.uuid4())

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    is_admin = data.get('is_admin', False)
    user, error_msg = register_new_user(data.get('username'), data.get('password'), is_admin)
    if error_msg:
        return error_response(error_msg, 400)
    return success_response({"message": "User registered successfully"}, 201)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return error_response("Username and password are required", 400)
    
    # Validate user credentials
    user, error_msg = validate_user_credentials(username, password)
    if error_msg:
        return error_response(error_msg, 401)

    # Generate a unique token for the session
    token = generate_token()
    print(f"Generated token for user {username}: {token}")  # Debugging output

    # Store the token in the user's document in the database
    try:
        result = mongo.cx.movies_db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"token": token}}
        )
        print("Token update result:", result.modified_count)  # Debugging output

        if result.modified_count == 0:
            return error_response("Failed to update user token", 500)
    except Exception as e:
        print("Error updating user token:", str(e))
        return error_response("An internal error occurred while updating token", 500)

    # Return the token to the client along with the user's role
    return success_response({
        "access_token": token,
        "role": "admin" if user.get("is_admin") else "user"
    }, 200)

@user_bp.route('/profile', methods=['GET'])
@token_required
def profile():
    user_data = request.user  # Access user data if needed
    user = get_user_profile(user_data["_id"])
    return success_response(user)

@user_bp.route('/watchlist', methods=['GET'])
@token_required
def get_watchlist():
    user_data = request.user
    movies = get_user_watchlist(user_data["_id"])
    return success_response({"watchlist": movies})

@user_bp.route('/watchlist', methods=['POST'])
@token_required
def add_to_watchlist():
    movie_id = request.json.get('movie_id')
    user_data = request.user
    result, error_msg = add_movie_to_watchlist(user_data["_id"], movie_id)
    if error_msg:
        return error_response(error_msg, 404)
    return success_response({"message": result})

@user_bp.route('/watchlist', methods=['DELETE'])
@token_required
def remove_from_watchlist():
    movie_id = request.json.get('movie_id')
    user_data = request.user
    result, error_msg = remove_movie_from_watchlist(user_data["_id"], movie_id)
    return success_response({"message": result})

# Example of an admin-protected route
@user_bp.route('/admin-dashboard', methods=['GET'])
@token_required
def admin_dashboard():
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    # Admin-specific logic here
    return jsonify({"message": "Welcome to the admin dashboard"})
