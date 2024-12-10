from extensions import mongo
from models.user import User
from datetime import datetime, timezone, timedelta
from bson.objectid import ObjectId
from utils.helpers import is_valid_object_id

def register_new_user(username, password, is_admin=False):
    if mongo.cx.movies_db.users.find_one({"username": username}):
        return None, "User already exists"
    password_hash = User.hash_password(password)
    user = {
        "username": username,
        "password_hash": password_hash,
        "is_admin": is_admin,  # Save the is_admin flag
        "watchlist": [],
        "failed_attempts": 0,
        "account_locked": False
    }
    mongo.cx.movies_db.users.insert_one(user)
    return user, None

def validate_user_credentials(username, password):
    user = mongo.cx.movies_db.users.find_one({"username": username})
    print("User found for validation:", user)  # Debugging output

    if not user:
        return None, "Invalid username or password."

    if user.get("account_locked", False):
        lock_time = user.get("lock_time")
        if lock_time and datetime.now(timezone.utc) - lock_time < timedelta(minutes=15):
            return None, "Account is locked. Please try again later."
        
        mongo.cx.movies_db.users.update_one({"_id": user["_id"]}, {
            "$set": {"failed_attempts": 0},
            "$unset": {"account_locked": "", "lock_time": ""}
        })

    if User.check_password(user["password_hash"], password):
        mongo.cx.movies_db.users.update_one({"_id": user["_id"]}, {
            "$set": {"failed_attempts": 0},
            "$unset": {"account_locked": "", "lock_time": ""}
        })
        return user, None
    
    failed_attempts = user.get("failed_attempts", 0) + 1
    update_fields = {"failed_attempts": failed_attempts}
    if failed_attempts >= 5:
        update_fields["account_locked"] = True
        update_fields["lock_time"] = datetime.now(timezone.utc)
    mongo.cx.movies_db.users.update_one({"_id": user["_id"]}, {"$set": update_fields})
    return None, "Invalid username or password."

def get_user_profile(user_id):
    user = mongo.cx.movies_db.users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
    if not user:
        return None, "User not found"
    return user, None

def add_movie_to_watchlist(user_id, movie_id):
    # Validate user_id as ObjectId
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return None, "Invalid user ID"

    # Validate movie_id as ObjectId
    try:
        movie_object_id = ObjectId(movie_id)
        print(f"Converted movie_id to ObjectId: {movie_object_id}")
    except Exception:
        return None, "Invalid movie ID"

    # Check if the movie exists in the "movies" collection by _id
    movie_exists = mongo.cx.movies_db.movies.find_one({"_id": movie_object_id})
    print(f"Movie found: {movie_exists}")  # Debug print to confirm movie existence
    if not movie_exists:
        return None, "Movie not found"

    # Add the movie's ObjectId to the user's watchlist
    result = mongo.cx.movies_db.users.update_one(
        {"_id": user_object_id},
        {"$addToSet": {"watchlist": movie_object_id}}  # Add ObjectId directly
    )

    # Return success message based on the update operation
    return "Movie added to watchlist" if result.modified_count > 0 else "Movie already in watchlist", None

def remove_movie_from_watchlist(user_id, movie_id):
    result = mongo.cx.movies_db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"watchlist": movie_id}}
    )
    return "Movie removed from watchlist" if result.modified_count > 0 else "Movie not in watchlist", None

def get_user_watchlist(user_id):
    user = mongo.cx.movies_db.users.find_one({"_id": ObjectId(user_id)})
    if not user or "watchlist" not in user:
        return [], "No watchlist found for user"
    movie_ids = user["watchlist"]
    movies = list(mongo.cx.movies_db.movies.find({"_id": {"$in": [ObjectId(mid) for mid in movie_ids]}}))
    for movie in movies:
        movie["_id"] = str(movie["_id"])
    return movies
