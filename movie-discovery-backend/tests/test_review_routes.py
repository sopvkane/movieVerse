import pytest
from extensions import mongo
from .test_utils import register_user, login_user

def test_add_review(client):
    # Register user and check response
    register_response = register_user(client, 'testuser', 'Password123!')
    print("Register response:", register_response.get_json())  # Debugging output
    assert register_response.status_code == 201

    # Log in user and check token
    token = login_user(client, 'testuser', 'Password123!')
    print("Token:", token)  # Debugging output

    # Verify movie ID and submit review
    movie_id = "507f1f77bcf86cd799439011"
    response = client.post(
        f'/api/v1/movies/{movie_id}/review',
        headers={'Authorization': f'Bearer {token}'},
        json={'rating': 4, 'review': 'Great movie!'}
    )
    assert response.status_code == 201

def test_get_reviews(client):
    movie = mongo.cx.movies_db.movies.find_one({"title": "Inception"})
    movie_id = movie["_id"] if movie else mongo.cx.movies_db.movies.insert_one({
        "title": "Inception", "genres": ["Sci-Fi"], "description": "A mind-bending thriller"
    }).inserted_id

    register_response = register_user(client, 'reviewuser', 'SecurePass123!')
    assert register_response.status_code == 201
    token = login_user(client, 'reviewuser', 'SecurePass123!')

    client.post(
        f'/api/v1/movies/{movie_id}/review',
        headers={'Authorization': f'Bearer {token}'},
        json={'rating': 4, 'review': 'Great movie!'}
    )

    response = client.get(f'/api/v1/movies/{movie_id}/reviews')
    assert response.status_code == 200
    reviews = response.get_json()
    assert isinstance(reviews, list) and len(reviews) > 0
