from flask import Flask
from extensions import mongo, limiter
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from config import config
from scripts.populate_movies import populate_movies  # Import the populate function
from scripts.update_genre_format import update_genre_format  # Import the genre update function

# Import blueprints
from routes.user_routes import user_bp
from routes.movie_routes import movie_bp
from routes.review_routes import review_bp
from routes.analytics_routes import analytics_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    mongo.init_app(app)
    JWTManager(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    # Populate the movies database if needed
    with app.app_context():
        populate_movies()
        update_genre_format()  # Call the genre update function here

    # Register blueprints with API versioning prefix
    api_prefix = '/api/v1.0'
    app.register_blueprint(user_bp, url_prefix=f'{api_prefix}/users')
    app.register_blueprint(movie_bp, url_prefix=f'{api_prefix}/movies')
    app.register_blueprint(review_bp, url_prefix=f'{api_prefix}/movies/')
    app.register_blueprint(analytics_bp, url_prefix=f'{api_prefix}/analytics')

    # Swagger Configuration
    Swagger(app)

    return app

    @app.route('/test_cors')
    def test_cors():
        return {"message": "CORS test"}


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
