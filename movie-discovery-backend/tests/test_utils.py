# tests/test_utils.py
import json

def register_user(client, username, password, is_admin=False):
    return client.post(
        '/api/v1/users/register',
        json={
            "username": username,
            "password": password,
            "is_admin": is_admin
        }
    )

def login_user(client, username, password):
    response = client.post(
        '/api/v1/users/login',
        json={
            "username": username,
            "password": password
        }
    )
    if response.status_code == 200:
        return response.get_json()["access_token"]
    return None
