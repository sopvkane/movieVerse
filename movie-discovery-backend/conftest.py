import pytest
from app import create_app
from extensions import mongo
from bson.objectid import ObjectId

@pytest.fixture(scope="module")
def app():
    # Set up the app with a 'testing' configuration
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        with app.app_context():
            # Ensure we're working in the test database
            movies_db = mongo.cx.movie_db_test

            # Insert initial test data
            movies_db.movies.insert_one({
                "title": "Inception",
                "genres": ["Action", "Sci-Fi"],
                "rating": 8.8,
                "year": 2010,
                "runtime": 148,
                "description": "A mind-bending thriller.",
                "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
                "director": "Christopher Nolan"
            })

            movies_db.movies.insert_one({
                "title": "The Matrix",
                "genres": ["Sci-Fi"],
                "rating": 8.7,
                "year": 1999,
                "runtime": 136,
                "description": "A hacker discovers a mind-bending reality.",
                "actors": ["Keanu Reeves"],
                "director": "Lana Wachowski"
            })

        yield client

@pytest.fixture
def auth_headers(client):
    mongo.cx.movie_db_test.users.delete_many({"username": "testuser"})
    client.post('/api/v1/users/register', json={"username": "testuser", "password": "Password123!"})
    login_response = client.post('/api/v1/users/login', json={"username": "testuser", "password": "Password123!"})
    token = login_response.get_json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(client):
    mongo.cx.movie_db_test.users.delete_many({"username": "admin"})
    client.post('/api/v1/users/register', json={"username": "admin", "password": "AdminPass123!", "is_admin": True})
    login_response = client.post('/api/v1/users/login', json={"username": "admin", "password": "AdminPass123!"})
    token = login_response.get_json().get("access_token")
    return {"Authorization": f"Bearer {token}"}
