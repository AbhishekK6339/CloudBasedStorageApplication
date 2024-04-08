from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.mongo import mongo

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate password and confirm password
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('auth.signup'))

        # Check if username or email already exists
        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            flash('Username or email already exists. Please choose different ones.', 'error')
            return redirect(url_for('auth.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Store user data in the database
        try:
            mongo.db.users.insert_one({'username': username, 'email': email, 'password': hashed_password})
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('An error occurred while creating your account. Please try again later.', 'error')
            app.logger.error(f"Error creating user: {e}")

    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username exists in the database
        user = mongo.db.users.find_one({'username': username})
        if not user:
            flash('No user found with this username. Please sign up first.', 'error')
            return redirect(url_for('auth.login'))

        # Validate password
        if not check_password_hash(user['password'], password):
            flash('Invalid password. Please try again.', 'error')
            return redirect(url_for('auth.login'))

        # Login successful
        session['logged_in'] = True
        session['username'] = username  # Optionally store username in session
        flash('Login successful!', 'success')
        return redirect(url_for('upload.upload'))

    return render_template('login.html')

@auth_blueprint.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)  # Clear username from session if stored
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))