from flask import Blueprint

upload_blueprint = Blueprint('upload', __name__)

# Import routes from routes.py
from app.upload import routes
