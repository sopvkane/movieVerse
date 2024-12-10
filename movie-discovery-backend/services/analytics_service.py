from extensions import mongo
from bson.objectid import ObjectId

def get_top_genres():
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
        {"$unwind": "$genres"},
        {"$group": {
            "_id": "$genres",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    # Log the pipeline to inspect
    print("Aggregation Pipeline:", pipeline)

    # Execute the pipeline
    genres = list(mongo.cx.movies_db.movies.aggregate(pipeline))

    # Log the output from the aggregation
    print("Genres found:", genres)

    return [{"genre": item["_id"], "count": item["count"]} for item in genres]

def get_average_ratings_by_year():
    pipeline = [
        {"$match": {
            "year": {"$ne": None}, 
            "imdb_rating": {"$ne": None}  # Change here to use imdb_rating
        }},
        {"$group": {
            "_id": "$year", 
            "average_rating": {"$avg": "$imdb_rating"}  # Change here to use imdb_rating
        }},
        {"$sort": {"_id": 1}}
    ]
    
    ratings_by_year = list(mongo.cx.movies_db.movies.aggregate(pipeline))
    
    # Print raw output for debugging
    print("Raw ratings_by_year from aggregation:", ratings_by_year)  # Debugging
    
    return [{"year": item["_id"], "average_rating": item["average_rating"]} for item in ratings_by_year]

def get_top_rated_by_genre():
    pipeline = [
        {"$unwind": "$genre"},  # Changed from genres to genre
        {"$sort": {"imdb_rating": -1}},  # Ensure we're sorting by the correct rating field
        {"$group": {
            "_id": "$genre",  # Group by genre
            "title": {"$first": "$name"},  # Use the field name correctly
            "rating": {"$first": "$imdb_rating"},  # Reference imdb_rating instead of rating
            "year": {"$first": "$year"}  # Ensure year is included
        }},
        {"$sort": {"_id": 1}}  # Sort by genre name
    ]
    
    top_rated = list(mongo.cx.movies_db.movies.aggregate(pipeline))
    
    # Debugging output
    print("Top rated movies by genre:", top_rated)
    
    return [{"genre": item["_id"], "title": item["title"], "rating": item["rating"], "year": item["year"]} for item in top_rated]

def get_average_duration_by_genre():
    pipeline = [
        {"$unwind": "$genre"},  # Make sure this is the correct field in your documents
        {"$group": {
            "_id": "$genre",  # Group by genre
            "average_duration": {"$avg": "$duration"}  # Calculate average duration
        }},
        {"$sort": {"average_duration": -1}}  # Sort by average duration
    ]
    
    duration_by_genre = list(mongo.cx.movies_db.movies.aggregate(pipeline))
    
    # Debugging output
    print("Average duration by genre:", duration_by_genre)
    
    return [{"genre": item["_id"], "average_duration": item["average_duration"]} for item in duration_by_genre]

