# utils/serialize.py

from bson import ObjectId

def serialize_movie(movie):
    return {
        '_id': str(movie['_id']),
        'title': movie.get('title'),
        'year': movie.get('year'),
        'genres': movie.get('genres', []),
        'runtime': movie.get('runtime'),
        'actors': movie.get('actors', []),
        'director': movie.get('director'),
        'description': movie.get('description'),
        'rating': movie.get('rating', 0)  # Assuming 'rating' field exists
        # Add other fields as necessary
    }
