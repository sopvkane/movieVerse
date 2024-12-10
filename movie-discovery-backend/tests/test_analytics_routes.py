import pytest
from app import create_app
from extensions import mongo
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
            with app.app_context():
                # Clear collections in the test database
                mongo.db.users.delete_many({})
                mongo.db.movies.delete_many({})
                mongo.db.reviews.delete_many({})
                
                # Insert initial test data if needed
                yield client

def test_top_genres(client):
    with client.application.app_context():
        mongo.cx.movies_db.movies.insert_many([
            {"title": "Movie A", "genres": ["Action"], "rating": 4.5},
            {"title": "Movie B", "genres": ["Drama"], "rating": 3.8},
            {"title": "Movie C", "genres": ["Action", "Drama"], "rating": 4.0}
        ])
    response = client.get('/api/v1/analytics/top-genres')
    assert response.status_code == 200
    data = response.get_json().get('genres')
    assert isinstance(data, list) and len(data) > 0

def test_average_ratings_by_year(client):
    with client.application.app_context():
        mongo.cx.movies_db.movies.insert_many([
            {"title": "Movie A", "year": 2020, "rating": 4.5},
            {"title": "Movie B", "year": 2021, "rating": 3.8},
            {"title": "Movie C", "year": 2020, "rating": 4.0}
        ])
    response = client.get('/api/v1/analytics/average-ratings-by-year')
    assert response.status_code == 200
    data = response.get_json().get('ratings_by_year')
    assert isinstance(data, list) and len(data) > 0

def test_top_rated_by_genre(client):
    with client.application.app_context():
        mongo.cx.movies_db.movies.insert_many([
            {"title": "Movie A", "genres": ["Action"], "rating": 4.5},
            {"title": "Movie B", "genres": ["Drama"], "rating": 3.8},
            {"title": "Movie C", "genres": ["Action"], "rating": 5.0}
        ])
    response = client.get('/api/v1/analytics/top-rated-by-genre')
    assert response.status_code == 200
    data = response.get_json().get('top_movies')
    assert isinstance(data, list) and len(data) > 0
