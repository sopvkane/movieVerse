from flask import Blueprint, request
from utils.auth import token_required, is_admin
from utils.helpers import success_response, error_response, get_user_from_token
from services.movie_service import (
    get_movie_by_id,
    search_movies,
    get_content_based_recommendations,
    filter_movies,
    add_movie,
    get_categories
)
from schemas.movie_schema import MovieSchema
from marshmallow import ValidationError
from bson.objectid import ObjectId
from extensions import mongo


movie_bp = Blueprint('movie_bp', __name__)
movie_schema = MovieSchema()

# Search movies with optional filters, pagination, and advanced options
@movie_bp.route('/search', methods=['GET'])
def advanced_search():
    actor = request.args.get('actor')
    genre = request.args.get('genre')
    director = request.args.get('director_name')
    rating = request.args.get('rating', type=float)  # Use type=float for automatic conversion

    # Construct the filters dictionary
    filters = {
        "actor": actor,
        "genre": genre,
        "director_name": director,
        "rating": rating
    }

    movies, total_movies = search_movies(filters)
    return success_response({
        "movies": movies,
        "total": total_movies
    })

# Get movie details by ID
@movie_bp.route('/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie, error_msg = get_movie_by_id(movie_id)
    if error_msg:
        return error_response(error_msg, 404)
    return success_response(movie)

# Get all movies or filtered search
@movie_bp.route('/', methods=['GET'])
def get_movies():
    print("Request args:", request.args)  # Debugging

    all_param = request.args.get('all', 'false').lower() == 'true'
    query_params = request.args.to_dict()  # Explicitly convert to dictionary
    print("Converted query_params:", query_params)  # Debugging

    movies = []
    if all_param:
        # Return all movies if 'all' is true
        movies, _ = search_movies({})  # No filters applied
    else:
        # Pass converted query_params to search_movies
        movies, _ = search_movies(query_params, page=1, per_page=10)

    return success_response(movies)

# Get content-based recommendations for a specific movie by ID
@movie_bp.route('/<movie_id>/recommendations', methods=['GET'])
def recommendations(movie_id):
    recommendations, error_msg = get_content_based_recommendations(movie_id)
    if error_msg:
        return error_response(error_msg, 404)
    return success_response({"recommendations": recommendations})

# Create a new movie (for admin or setup purposes)
@movie_bp.route('/', methods=['POST'])
@token_required  # Ensure that user is authenticated
def create_movie():
    if not is_admin():
        return error_response("Admin access required", 403)
    
    try:
        data = request.get_json()
        validated_data = movie_schema.load(data)
        movie, error = add_movie(validated_data)
        if error:
            return error_response(error, 500)
        return success_response(movie, 201)
    except ValidationError as err:
        return error_response(err.messages, 400)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", 500)
    
# Update an existing movie by ID (admin only)
@movie_bp.route('/<movie_id>', methods=['PUT'])
@token_required  # Ensure that user is authenticated
def update_movie(movie_id):
    if not is_admin():
        return error_response("Admin access required", 403)

    data = request.get_json()
    if not data:
        return error_response("No input data provided", 400)

    print("Incoming data:", data)  # Debugging: Check what was received

    updated_fields = {}

    # Map incoming fields to the database structure
    if 'rating' in data:  # Field in the request is 'rating'
        updated_fields['rating'] = data.pop('rating')  # Keep as 'rating' to match schema
    if 'title' in data:
        updated_fields['title'] = data.pop('title')  # Map to 'title'
    if 'director' in data:
        updated_fields['director'] = data.pop('director')  # Map to 'director'
    if 'duration' in data:
        updated_fields['duration'] = data.pop('duration')  # Map to 'runtime'
    if 'genres' in data:
        updated_fields['genres'] = data.pop('genres')  # Map to 'genres'
    if 'actors' in data:
        updated_fields['actors'] = data.pop('actors')  # Map to 'actors'

    print("Updated fields before validation:", updated_fields)  # Debugging: Check fields to validate

    try:
        # Validate only the fields that were passed in
        validated_data = movie_schema.load(updated_fields, partial=True)

        print("Validated data:", validated_data)  # Debugging: Check validated data

        # Perform the update
        result = mongo.cx.movies_db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": validated_data})

        if result.matched_count == 0:
            return error_response("Movie not found", 404)

        updated_movie = mongo.cx.movies_db.movies.find_one({"_id": ObjectId(movie_id)})
        return success_response(movie_schema.dump(updated_movie))
    except ValidationError as err:
        print("Validation Error:", err.messages)  # Debugging: Log validation error messages
        return error_response(err.messages, 422)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", 500)

# Delete a movie by ID (admin only)
@movie_bp.route('/<movie_id>', methods=['DELETE'])
@token_required  # Ensure that user is authenticated
def delete_movie(movie_id):
    user_data = getattr(request, 'user', None)
    print("Current User Data:", user_data)  # Debugging output to check user info

    if not is_admin():
        return error_response("Admin access required", 403)

    result = mongo.cx.movies_db.movies.delete_one({"_id": ObjectId(movie_id)})
    if result.deleted_count == 0:
        return error_response("Movie not found", 404)
    return success_response({"message": "Movie deleted successfully"})

@movie_bp.route("/categories", methods=["GET"])
def get_movie_categories():
    """
    Endpoint to fetch movie categories (genres).
    """
    categories, error = get_categories()  # Fetch the categories using aggregation
    
    # Log for debugging
    print("Categories:", categories)
    print("Error:", error)
    
    if error:
        # If there is an error, return it with the proper response format
        return error_response({"error": error}), 500  # Make sure error_response returns a valid response

    # Return the success response
    response = success_response({"categories": categories})
    
    # Log the final response for debugging
    print("Final Success Response:", response)
    
    return response  # Return the actual response object from success_response


