import pytest
from bson.objectid import ObjectId
from extensions import mongo
from .test_utils import login_user

def test_search_movies(client):
    # Ensure the collection is empty or delete any previous data with "Inception" to avoid duplicates
    mongo.cx.movies_db.movies.delete_many({"title": "Inception"})
    
    # Insert a single movie entry for testing
    movie_data = {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "title": "Inception",
        "genres": ["Action", "Sci-Fi"],
        "rating": 8.8,
        "year": 2010,
        "runtime": 148,
        "description": "A mind-bending thriller.",
        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
        "director": "Christopher Nolan"
    }
    mongo.cx.movies_db.movies.insert_one(movie_data)
    
    # Perform the search
    response = client.get('/api/v1/movies/?title=Inception')
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    # Verify the search results
    data = response.get_json().get('movies')
    assert isinstance(data, list), "Expected data to be a list"
    assert len(data) == 1, f"Expected 1 result, got {len(data)}"
    assert data[0]['title'] == 'Inception', f"Expected title 'Inception', got {data[0]['title'] if data else 'None'}"

def test_get_movie_details(client):
    movie = mongo.cx.movies_db.movies.find_one({"title": "Inception"})
    movie_id = str(movie['_id'])
    response = client.get(f'/api/v1/movies/{movie_id}')
    assert response.status_code == 200
    assert response.get_json().get('title') == 'Inception'

def test_content_based_recommendations(client):
    mongo.cx.movies_db.movies.delete_many({})
    mongo.cx.movies_db.movies.insert_many([
        {"title": "Inception", "genres": ["Action", "Sci-Fi"], "year": 2010, "description": "A thriller."},
        {"title": "Interstellar", "genres": ["Adventure", "Sci-Fi", "Drama"], "year": 2014, "description": "Stars."},
        {"title": "The Matrix", "genres": ["Action", "Sci-Fi"], "year": 1999, "description": "Reality."}
    ])
    movie = mongo.cx.movies_db.movies.find_one({"title": "Inception"})
    test_movie_id = str(movie['_id'])
    response = client.get(f'/api/v1/movies/{test_movie_id}/recommendations')
    assert response.status_code == 200
    recommendations = response.get_json().get('recommendations')
    assert isinstance(recommendations, list) and len(recommendations) > 0

def test_create_movie_as_admin(client, admin_headers):
    new_movie = {
        "title": "New Movie",
        "genres": ["Drama"],
        "runtime": 120,
        "actors": ["Actor1", "Actor2"],
        "director": "Director1",
        "release_year": 2021,
        "description": "A new movie",
        "rating": 7.5
    }
    response = client.post('/api/v1/movies/', json=new_movie, headers=admin_headers)
    assert response.status_code == 201

def test_update_movie_as_admin(client, admin_headers):
    movie = mongo.cx.movies_db.movies.find_one({"title": "Inception"})
    movie_id = str(movie['_id'])
    response = client.put(
        f'/api/v1/movies/{movie_id}',
        json={
            "title": "Inception",
            "description": "Updated description",
            "director": "Christopher Nolan",
            "actors": ["Leonardo DiCaprio"],
            "genres": ["Sci-Fi", "Thriller"],
            "release_year": 2010,
            "runtime": 148,
            "rating": 9.0
        },
        headers=admin_headers
    )
    assert response.status_code == 200

def test_search_by_actor(client):
    response = client.get('/api/v1/movies/search?actor=Leonardo DiCaprio')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) and len(data) > 0
