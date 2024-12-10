# utils/validators.py

import re
from bson.objectid import ObjectId

def is_password_strong(password):
    """
    Validates if a password is strong.
    A strong password must be at least 8 characters long and include at least one uppercase letter,
    one lowercase letter, one digit, and one special character.
    """
    pattern = re.compile(r"""
        ^                   # Start of string
        (?=.*[A-Z])         # At least one uppercase letter
        (?=.*[a-z])         # At least one lowercase letter
        (?=.*\d)            # At least one digit
        (?=.*[@$!%*?&])     # At least one special character
        [A-Za-z\d@$!%*?&]{8,}  # Allowed characters, at least 8 characters long
        $                   # End of string
        """, re.VERBOSE)
    return pattern.match(password) is not None

def is_valid_objectid(id_str):
    """Checks if the provided string is a valid MongoDB ObjectId."""
    return ObjectId.is_valid(id_str)

def validate_movie_id(movie_id):
    """Validates that the movie_id is a valid ObjectId."""
    return is_valid_objectid(movie_id)

def validate_query_params(args):
    """Validates query parameters for the search_movies endpoint."""
    # Validate min_runtime and max_runtime
    min_runtime = args.get('min_runtime', type=int)
    max_runtime = args.get('max_runtime', type=int)
    if min_runtime is not None and min_runtime < 0:
        return "min_runtime must be a non-negative integer"
    if max_runtime is not None and max_runtime < 0:
        return "max_runtime must be a non-negative integer"
    if min_runtime is not None and max_runtime is not None and min_runtime > max_runtime:
        return "min_runtime cannot be greater than max_runtime"

    # Validate page and per_page
    page = args.get('page', type=int)
    per_page = args.get('per_page', type=int)
    if page is not None and page < 1:
        return "page must be a positive integer"
    if per_page is not None and per_page < 1:
        return "per_page must be a positive integer"

    # Validate genres and actors (ensure they are lists of strings)
    genres = args.getlist('genre')
    if genres and not all(isinstance(genre, str) for genre in genres):
        return "genre must be a list of strings"
    actors = args.getlist('actor')
    if actors and not all(isinstance(actor, str) for actor in actors):
        return "actor must be a list of strings"

    # Validate director and title (ensure they are strings)
    director = args.get('director')
    if director and not isinstance(director, str):
        return "director must be a string"
    title = args.get('title')
    if title and not isinstance(title, str):
        return "title must be a string"

    return None
