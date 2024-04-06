# app/__init__.py

from flask import Flask, redirect, url_for
from app.auth.routes import auth_blueprint
from app.mongo import init_mongo
import os

app = Flask(__name__)

# Define the MongoDB URI for local MongoDB instance
mongo_uri = "mongodb+srv://storage:Abhey123@cluster0.i4dedvi.mongodb.net/database"

# Set the MongoDB URI in the Flask app configuration
app.config["MONGO_URI"] = mongo_uri

# secretkey
app.config['SECRET_KEY'] = os.urandom(24)



# Initialize MongoDB connection
init_mongo(app)

# Register the authentication blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Define a route for the root URL
@app.route('/')
def index():
    return redirect(url_for('auth.signup'))  # Redirect to signup page when accessing root URL

if __name__ == "__main__":
    app.run(debug=True)
