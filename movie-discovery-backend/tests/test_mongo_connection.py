import pytest
from app import create_app
from extensions import mongo

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            mongo.db.movies.delete_many({})
        yield client


def test_mongo_connection(client, app):
    with app.app_context():
        db_name = app.config["MONGO_DBNAME"]
        assert mongo.db.name == db_name, f"Expected MongoDB to be connected to '{db_name}' but got '{mongo.db.name}'"
