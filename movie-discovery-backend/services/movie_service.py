import re
from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd  # Import pandas
from extensions import mongo

# movie_service.py

import re
from bson.objectid import ObjectId
from extensions import mongo

import re
from bson.objectid import ObjectId
from extensions import mongo

import re
from bson.objectid import ObjectId
from extensions import mongo

def search_movies(query_params, page=1, per_page=20):
    print("Received query_params:", query_params)
    query = {}

    # Title search with case-insensitive regex
    if "title" in query_params and query_params["title"]:
        query["name"] = {"$regex": re.escape(query_params["title"]), "$options": "i"}

    # Genre search with case-insensitive matching
    if "genre" in query_params and query_params["genre"]:
        query["genre"] = {"$in": [query_params["genre"].strip()]}

    # Actor search within the cast_name array
    if "actor" in query_params and query_params["actor"]:
        actor_name = query_params["actor"].strip()
        query["cast_name"] = {"$in": [actor_name]}

    # Director search with case-insensitive regex
    if "director_name" in query_params and query_params["director_name"]:
        query["director_name"] = {"$regex": re.escape(query_params["director_name"]), "$options": "i"}

    # IMDb rating filter as minimum rating
    if "rating" in query_params and query_params["rating"]:
        try:
            min_rating = float(query_params["rating"])
            query["imdb_rating"] = {"$gte": min_rating}
        except ValueError:
            pass  # Ignore invalid rating input

    # Debugging: Print the constructed query
    print("Constructed movie Query:", query)

    skip = (page - 1) * per_page
    try:
        movies_cursor = mongo.cx.movies_db.movies.find(query).skip(skip).limit(per_page)
        movies = [{"_id": str(movie["_id"]), **movie} for movie in movies_cursor]
        total = mongo.cx.movies_db.movies.count_documents(query)
    except Exception as e:
        return None, f"Database error occurred: {e}"

    print(f"Total Movies Found: {total}")
    return movies, total


def get_movie_by_id(movie_id):
    """
    Retrieves a movie by its ID.
    """
    if not ObjectId.is_valid(movie_id):
        return None, "Invalid movie ID"
    
    try:
        movie = mongo.cx.movies_db.movies.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            return None, "Movie not found"
        movie["_id"] = str(movie["_id"])
    except Exception as e:
        return None, f"Database error occurred: {e}"
    
    return movie, None

def get_categories():
    """
    Fetches categories (genres) for movies using aggregation to ensure correct format.
    """
    try:
        # Use aggregation to get the top genres with counts
        pipeline = [
            {
                "$project": {
                    "genres": {
                        "$cond": {
                            "if": {"$eq": [{"$type": "$genre"}, "array"]},  # Check if genre is an array
                            "then": "$genre",  # If true, keep it as is
                            "else": {"$split": ["$genre", ","]}  # Otherwise, split the string
                        }
                    }
                }
            },
            {"$unwind": "$genres"},  # Flatten the genres
            {"$group": {
                "_id": "$genres",  # Group by the genre
                "count": {"$sum": 1}  # Count occurrences
            }},
            {"$sort": {"count": -1}},  # Sort by the count (descending)
            {"$limit": 10}  # Limit to top 10 genres
        ]

        # Execute the pipeline
        genres = list(mongo.cx.movies_db.movies.aggregate(pipeline))

        # Format the result for the response
        categories = [{"key": genre["_id"].lower(), "name": genre["_id"]} for genre in genres]

        return categories, None  # Return the categories and no error
    except Exception as e:
        return None, f"Database error occurred while fetching categories: {e}"  # Return error message


def add_movie(movie_data):
    """
    Adds a new movie to the database.
    """
    try:
        result = mongo.cx.movies_db.movies.insert_one(movie_data)
        movie_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string for JSON serialization
        return movie_data, None  # Return the movie data and None for the error
    except Exception as e:
        print("Error while adding movie:", e)  # Debug output
        return None, f"Database error occurred while adding movie: {e}"


def get_content_based_recommendations(movie_id):
    """
    Generates content-based recommendations for a given movie ID.
    """
    try:
        movie_id = ObjectId(movie_id)
    except Exception as e:
        return None, f"Invalid movie ID format: {e}"

    try:
        movies = list(mongo.cx.movies_db.movies.find())
        if not movies:
            return None, "No movies found in the database."
    except Exception as e:
        return None, f"Database error occurred: {e}"

    df = pd.DataFrame(movies)
    
    df["description"] = df.get("description", "").fillna("")
    df["genres"] = df["genres"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

    combined_features = df["description"] + " " + df["genres"]

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(combined_features)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df["_id"]).drop_duplicates()
    idx = indices.get(movie_id)
    
    if idx is None:
        return None, "Movie ID not found for recommendation."

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]

    recommendations = df.iloc[movie_indices].to_dict("records")
    
    for rec in recommendations:
        rec["_id"] = str(rec["_id"])
    
    return recommendations, None

def filter_movies(filters):
    """
    Filters movies based on various parameters: genre, actor, director, duration, release year.
    """
    query = {}

    if "genre" in filters and filters["genre"]:
        query["genres"] = filters["genre"]
    if "actor" in filters and filters["actor"]:
        query["actors"] = filters["actor"]
    if "director" in filters and filters["director"]:
        query["director"] = filters["director"]
    if "duration" in filters and filters["duration"]:
        query["duration"] = {"$lte": filters["duration"]}
    if "release_year" in filters and filters["release_year"]:
        query["release_year"] = filters["release_year"]

    try:
        movies = list(mongo.cx.movies_db.movies.find(query))
        for movie in movies:
            movie["_id"] = str(movie["_id"])
    except Exception as e:
        return None, f"Database error occurred: {e}"

    return movies
