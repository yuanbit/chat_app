# Main application
import os
import time
from flask import Flask, render_template, redirect, url_for, flash, request, session, Response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from aylienapiclient import textapi

from wtform_fields import *
from db import *

# Aylien for sentiment analysis
client = textapi.Client("44c6b5b6", "f88daf87ca37572a813da7425a46685b")

# Configure app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Initialize database
db = SQLAlchemy(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Current time
time_stamp = time.strftime('%b %d, %Y %I:%M:%S %p', time.localtime())

# Configure flask login
login = LoginManager(app)

# Initialize app
login.init_app(app)

# Load users
@login.user_loader
def load_user(id):
    # Get id using SQLAlchemy
    return User.query.get(int(id))

# Route for home/registration page
@app.route("/", methods=['GET', 'POST'])
def index():
    """ Renders the flask WTForms fields for user registration """

    # Initialize registration form
    reg_form = RegistrationForm()

    # Update DB if validation success
    if reg_form.validate_on_submit():
        # Obtain data from fields using flask wtforms
        first_name = reg_form.first_name.data
        last_name = reg_form.last_name.data
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data

        # Hash plain text password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # User data
        user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_pswd)

        # Add and commit user to database
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully. Please login.', 'success')
        # Redirect user to login page if successful registration
        return redirect(url_for('login'))

    # Display registration page if not successful
    return render_template("index.html", form=reg_form)

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():

    # Initialize login form
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():

        # Get email submitted in login form from DB
        user_object = User.query.filter_by(email=login_form.email.data).first()
        # Load user to login
        login_user(user_object)
        # Redirect user to chat route
        return redirect(url_for('chat'))
    # Stay on login page if not successful
    return render_template("login.html", form=login_form)

# Route for chat page
@app.route("/chat", methods=['GET', 'POST'])
def chat():
    # If user is not logged in
    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        # Redirect to login page
        return redirect(url_for('login'))
    # Display chat page
    return render_template('chat.html', username=current_user.username)

# Route for logout
@app.route("/logout", methods=['GET'])
@login_required
def logout():

    # Log user out
    logout_user()
    flash('You have logged out successfully.', 'success')
    # Redirect to login page
    return redirect(url_for('login'))

# Route for non-existent pages
@app.errorhandler(404)
def page_not_found():
    # Set 404 status and display error page
    return render_template('404.html'), 404

# Tell SocketIO what actions to take when clients send message to an event bucket
@socketio.on('message')
def message(data):
    """ Event handler for incoming messages """

    msg = data["msg"]
    username = data["username"]
    room = data["room"]

    # Detect sentiment of the incoming message
    sentiment = client.Sentiment({'text': msg})

    # Map sentiments
    if sentiment['polarity'] == "positive":
        msg += " :)"
    elif sentiment['polarity'] == "negative":
        msg += " :("
    else:
        msg += " :|"

    global time_stamp

    # Broadcast incoming message
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

# Create event handler when a user joins the chatroom
@socketio.on('join')
def handle_join_event(data):
    """ Event handler when a user joins the chatroom """

    username = data["username"]
    room = data["room"]

    # Join the chatroom
    join_room(room)

    time_stamp = time.strftime('%I:%M:%S %p', time.localtime())

    # Broadcast that new user has joined
    send({"msg": username + " joined at " + time_stamp}, room=room)


@socketio.on('leave')
def handle_leave_event(data):
    """ Event handler when a user leaves the chatroom """

    username = data['username']
    room = data['room']

    # Leave the chatroom
    leave_room(room)

    time_stamp = time.strftime('%I:%M:%S %p', time.localtime())

    # Broadcast that a user has left
    send({"msg": username + " left at " + time_stamp}, room=room)

if __name__ == "__main__":

    app.run()
