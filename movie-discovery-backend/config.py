# config.py

from datetime import timedelta

class Config:
    SECRET_KEY = 'your_secret_key'
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/movie_db'  # Default MongoDB URI

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    MONGO_DBNAME = "movie_db_test"
    DEBUG = False
    MONGO_URI = 'mongodb://localhost:27017/movie_db_test'  # Use a separate test database
    RATELIMIT_ENABLED = False  # Disable rate limiting in tests

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    MONGO_URI = 'mongodb://localhost:27017/movie_db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
