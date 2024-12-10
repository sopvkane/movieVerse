from flask import Blueprint
from utils.helpers import success_response, error_response
from services.analytics_service import (
    get_top_genres, 
    get_average_ratings_by_year, 
    get_top_rated_by_genre, 
    get_average_duration_by_genre
)

analytics_bp = Blueprint('analytics_bp', __name__)

@analytics_bp.route('/top-genres', methods=['GET'])
def top_genres():
    try:
        genres = get_top_genres()  # Call the service function to get top genres
        return success_response({"genres": genres})
    except Exception as e:
        return error_response(str(e))

@analytics_bp.route('/average-ratings-by-year', methods=['GET'])
def average_ratings_by_year():
    ratings = get_average_ratings_by_year()
    return success_response({"ratings_by_year": ratings})

@analytics_bp.route('/top-rated-by-genre', methods=['GET'])
def top_rated_by_genre():
    top_movies = get_top_rated_by_genre()
    return success_response({"top_movies": top_movies})

@analytics_bp.route('/average-duration-by-genre', methods=['GET'])
def average_duration_by_genre():
    duration = get_average_duration_by_genre()
    return success_response({"duration_by_genre": duration})
