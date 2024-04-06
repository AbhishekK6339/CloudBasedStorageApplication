# auth/__init__.py

from flask import Blueprint

# Create a Blueprint object for the authentication routes
auth_blueprint = Blueprint('auth', __name__)

# Import the routes module to register the routes with the blueprint
from app.auth import routes
