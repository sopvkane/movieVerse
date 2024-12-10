# scripts/populate_movies.py

import json
from extensions import mongo
from bson.objectid import ObjectId

def safe_cast(value, target_type, default=None):
    """
    Safely cast a value to the target type. If the conversion fails (e.g., due to 'Nan'),
    return the provided default value.
    """
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default

def populate_movies():
    """
    Checks if the movies collection is populated with the initial 250 movies.
    If not, it loads data from movies.json and populates the collection.
    """
    movies_collection = mongo.cx.movies_db.movies

    # Check if there are fewer than 250 documents in the movies collection
    if movies_collection.count_documents({}) < 250:
        print("Movies collection is incomplete. Populating from movies.json...")
        
        # Load movies from movies.json
        try:
            with open('/Users/svkane/Desktop/Uni/archive/movies.json', 'r') as file:
                movies = json.load(file)
                
                for movie in movies:
                    # Ensure unique _id
                    movie["_id"] = ObjectId()

                    # Use safe casting for fields with potential 'Nan' values
                    movie["year"] = safe_cast(movie.get("year"), int, 0)  # Default to 0 if invalid
                    movie["imdb_rating"] = safe_cast(movie.get("imdb_rating"), float, 0.0)  # Default to 0.0
                    movie["duration"] = safe_cast(movie.get("duration"), int, 0)  # Default to 0

                    # Convert comma-separated strings to lists
                    movie["genre"] = movie["genre"].split(",") if "genre" in movie and movie["genre"] != 'Nan' else []
                    movie["cast_id"] = movie["cast_id"].split(",") if "cast_id" in movie and movie["cast_id"] != 'Nan' else []
                    movie["cast_name"] = movie["cast_name"].split(",") if "cast_name" in movie and movie["cast_name"] != 'Nan' else []
                    movie["writter_name"] = movie["writter_name"].split(",") if "writter_name" in movie and movie["writter_name"] != 'Nan' else []
                    movie["writter_id"] = movie["writter_id"].split(",") if "writter_id" in movie and movie["writter_id"] != 'Nan' else []

                    # Check for existing movie by title and year
                    if not movies_collection.find_one({"name": movie["name"], "year": movie["year"]}):
                        movies_collection.insert_one(movie)
                        print(f"Inserted movie: {movie['name']} ({movie['year']})")  # Debugging output
                    else:
                        print(f"Movie already exists, skipping: {movie['name']} ({movie['year']})")  # Debugging output

                print("Movies collection populated successfully.")
        except Exception as e:
            print(f"Error populating movies collection: {e}")
    else:
        print("Movies collection is already populated.")

