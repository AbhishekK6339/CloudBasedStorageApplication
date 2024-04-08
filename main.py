from flask import Flask, redirect, url_for
from app.auth.routes import auth_blueprint
from app.upload.routes import upload_blueprint
from app import app, mongo

# Blueprint registration
# app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(upload_blueprint, url_prefix='/upload')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port='8080')
