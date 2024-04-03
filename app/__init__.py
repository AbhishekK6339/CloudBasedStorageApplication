# app/__init__.py

from flask import Flask
from app.auth.routes import auth_blueprint
from app.mongo import init_mongo

app = Flask(__name__)

# Define the MongoDB URI for local MongoDB instance
mongo_uri = "mongodb+srv://storageapp:Abhey123@cluster0.4xp0q36.mongodb.net/database"


# Set the MongoDB URI in the Flask app configuration
app.config["MONGO_URI"] = mongo_uri

# Initialize MongoDB connection
init_mongo(app)

# Register the authentication blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)
