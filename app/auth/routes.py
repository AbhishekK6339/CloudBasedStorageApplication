# app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please provide both username and password', 'error')
            return redirect(url_for('auth.signup'))

        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please provide both username and password', 'error')
            return redirect(url_for('auth.login'))

        user = mongo.db.users.find_one({'username': username})
        if not user or not check_password_hash(user['password'], password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

        # Login successful
        flash('Login successful!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')
