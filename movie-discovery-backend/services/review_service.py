from extensions import mongo
from bson.objectid import ObjectId

def add_review(movie_id, user_id, rating, review_text):
    """
    Adds a review to a specified movie by a specific user.
    """
    if not ObjectId.is_valid(movie_id):
        return None, "Invalid movie ID"
    if not ObjectId.is_valid(user_id):
        return None, "Invalid user ID"

    review = {
        "movie_id": ObjectId(movie_id),
        "user_id": ObjectId(user_id),
        "rating": rating,
        "review": review_text,
    }
    
    try:
        result = mongo.cx.movies_db.reviews.insert_one(review)
        review["_id"] = str(result.inserted_id)
    except Exception as e:
        return None, f"Database error occurred: {e}"

    return review, None

def get_reviews(movie_id):
    """
    Retrieves all reviews for a specified movie.
    """
    if not ObjectId.is_valid(movie_id):
        return [], "Invalid movie ID"

    try:
        reviews = list(mongo.cx.movies_db.reviews.find({"movie_id": ObjectId(movie_id)}))
        # Convert ObjectId to string for each review
        for review in reviews:
            review["_id"] = str(review["_id"])
        return reviews  # Return just the reviews
    except Exception as e:
        print(f"Error retrieving reviews: {e}")
        return None  # This will be handled in the route function


def update_review(movie_id, user_id, rating, review_text):
    """
    Updates a user's review for a specified movie.
    """
    if not ObjectId.is_valid(movie_id):
        return None, "Invalid movie ID"
    if not ObjectId.is_valid(user_id):
        return None, "Invalid user ID"

    try:
        review = mongo.cx.movies_db.reviews.find_one({"movie_id": ObjectId(movie_id), "user_id": ObjectId(user_id)})
        if not review:
            return None, "Review not found"

        update_fields = {}
        if rating is not None:
            update_fields["rating"] = rating
        if review_text:
            update_fields["review"] = review_text

        mongo.cx.movies_db.reviews.update_one({"_id": review["_id"]}, {"$set": update_fields})
        review.update(update_fields)
        review["_id"] = str(review["_id"])
    except Exception as e:
        return None, f"Database error occurred: {e}"

    return review, None

def delete_review(movie_id, user_id):
    """
    Deletes a user's review for a specified movie.
    """
    if not ObjectId.is_valid(movie_id):
        return "Review not found", "Invalid movie ID"
    if not ObjectId.is_valid(user_id):
        return "Review not found", "Invalid user ID"

    try:
        result = mongo.cx.movies_db.reviews.delete_one({"movie_id": ObjectId(movie_id), "user_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return "Review not found", None
    except Exception as e:
        return None, f"Database error occurred: {e}"

    return "Review deleted successfully", None
