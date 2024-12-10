import pytest
from extensions import mongo
from .test_utils import register_user, login_user
from datetime import time

def test_user_registration(client):
    username = f'testuser_{int(time.time())}'  # Unique username
    response = register_user(client, username, 'StrongPass123!')
    assert response.status_code == 201
    assert response.get_json().get('message') == 'User registered successfully'


def test_user_login(client):
    register_response = register_user(client, 'testloginuser', 'Password123!')
    assert register_response.status_code == 201
    login_token = login_user(client, 'testloginuser', 'Password123!')
    assert login_token

def test_admin_registration(client):
    admin_response = register_user(client, 'adminuser', 'AdminPass123!', is_admin=True)
    assert admin_response.status_code == 201
    assert admin_response.get_json().get('message') == 'User registered successfully'

def test_watchlist_management(client, auth_headers):
    movie_id = str(mongo.cx.movies_db.movies.insert_one({
        "title": "Inception",
        "genres": ["Action", "Sci-Fi"],
        "year": 2010
    }).inserted_id)
    response = client.post('/api/v1/users/watchlist', headers=auth_headers, json={'movie_id': movie_id})
    assert response.status_code == 200

    get_response = client.get('/api/v1/users/watchlist', headers=auth_headers)
    assert get_response.status_code == 200
    watchlist = get_response.get_json().get('watchlist', [])
    assert any(movie['_id'] == movie_id for movie in watchlist)
