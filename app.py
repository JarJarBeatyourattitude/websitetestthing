from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# Create an in-memory SQLite database
memory_db = sqlite3.connect(':memory:')

# Initialize the Flask-SQLAlchemy object
db = SQLAlchemy()

app = Flask(__name__)

# Connect Flask-SQLAlchemy to the in-memory SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Check which button was clicked
        if request.form['button'] == 'Sign Up':
            # If the "Sign Up" button was clicked, redirect to the signup page
            return redirect(url_for('signup'))
        else:
            # If the "Log In" button was clicked, redirect to the login page
            return redirect(url_for('login'))
    else:
        # If the request is a GET request, just render the homepage
        return render_template('homepage.html')

# Define the User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Import the User class in the Flask app file


def authenticate(username, password):
    # Query the database to get the user with the given username
    user = User.query.filter_by(username=username).first()
    if user:
        # If the user exists, check their password
        if user.password == password:
            # If the password is correct, return the user object
            return user
    # If the user doesn't exist or the password is incorrect, return None
    return None

def login_user(user):
    # Store the user's id in the session
    session['user_id'] = user.id

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the user's input from the form
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user
        user = authenticate(username, password)
        if user:
            # If the user is authenticated, log them in and redirect to the dashboard
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            # If the user is not authenticated, show an error message and ask them to try again
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    else:
        # If the request is a GET request, just render the login page
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the user's input from the form
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # If the username is taken, show an error message and ask the user to try again
            error = "That username is already taken"
            return render_template('signup.html', error=error)

        # If the username is not taken, create a new User object
        user = User(username=username, password=password)

        # Add the new user to the database
        db.session.add(user)
        db.session.commit()

        # Log the user in and redirect to the dashboard
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        # If the request is a GET request, just render the signup page
        return render_template('signup.html')

# Define the dashboard route
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # If the user is logged in, render the dashboard template
        return render_template('dashboard.html')
    else:
        # If the user is not logged in, redirect them to the login page
        return redirect(url_for('login_page'))