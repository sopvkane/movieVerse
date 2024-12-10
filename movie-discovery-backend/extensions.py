from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

# Initialize instances without attaching them to the app immediately
bcrypt = Bcrypt()
mongo = PyMongo()  # MongoDB instance

# Configure Redis client for rate limiting
redis_client = Redis(host='localhost', port=6379)

# Configure Limiter with Redis storage
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
)

def init_extensions(app):
    """
    Attach all Flask extensions to the app within an application factory context.
    """
    bcrypt.init_app(app)
    mongo.init_app(app)  # Now attaches PyMongo to the app instance
    limiter.init_app(app)
