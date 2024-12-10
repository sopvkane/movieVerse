from flask import Blueprint, request
from utils.helpers import success_response, error_response, get_user_from_token
from services.review_service import add_review, get_reviews, update_review, delete_review

review_bp = Blueprint('review_bp', __name__)

def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    user_data = get_user_from_token(token)
    return user_data["_id"] if user_data else None

@review_bp.route('/<movie_id>/review', methods=['POST'])
def add_movie_review(movie_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return error_response("Authentication required", 401)
    data = request.get_json()
    review, error_msg = add_review(movie_id, user_id, data.get('rating'), data.get('review'))
    if error_msg:
        return error_response(error_msg, 400)
    return success_response(review, 201)

@review_bp.route('/<movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    reviews = get_reviews(movie_id)
    
    if reviews is None:
        return error_response("Error retrieving reviews", 500)
    
    # Debugging: Print reviews before sending response
    print("Reviews to return:", reviews)
    
    return success_response(reviews)


@review_bp.route('/<movie_id>/review', methods=['PUT'])
def update_movie_review(movie_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return error_response("Authentication required", 401)
    data = request.get_json()
    review, error_msg = update_review(movie_id, user_id, data.get('rating'), data.get('review'))
    if error_msg:
        return error_response(error_msg, 400)
    return success_response(review)

@review_bp.route('/<movie_id>/review', methods=['DELETE'])
def delete_movie_review(movie_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return error_response("Authentication required", 401)
    result, error_msg = delete_review(movie_id, user_id)
    if error_msg:
        return error_response(error_msg, 400)
    return success_response({"message": result})
