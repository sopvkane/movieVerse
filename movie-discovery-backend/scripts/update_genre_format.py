# scripts/update_genre_format.py

from extensions import mongo
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def update_genre_format():
    try:
        # Find movies with the old genre format
        movies = mongo.cx.movies_db.movies.find({"genre": {"$exists": True}})
        for movie in movies:
            if isinstance(movie['genre'], str):  # Check if the genre is still a string
                # Split the string into a list
                new_genres = movie['genre'].split(',')
                # Update the movie with the new genre format
                mongo.cx.movies_db.movies.update_one({"_id": ObjectId(movie['_id'])}, {"$set": {"genres": new_genres}})
                logging.info("Updating genre format...")
        
        print("Genres updated successfully.")
    except Exception as e:
        logging.error(f"Error updating genres: {e}")
        print(f"Error updating genres: {e}")
