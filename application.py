import time
from flask import Flask, render_template, redirect, url_for, flash, request, session, Response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from aylienapiclient import textapi

from wtform_fields import *
from models import *

# Aylien client
client = textapi.Client("44c6b5b6", "f88daf87ca37572a813da7425a46685b")

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uglcakesytydkw:a531b221acaeaf035634fb709b4bbe8d84995411718c1101104d7866fdfcdc70@ec2-174-129-33-201.compute-1.amazonaws.com:5432/d1jr4qvs8g9vgl'

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

# Route for homepage/registration page
@app.route("/", methods=['GET', 'POST'])
def index():
    """ Renders the fields """

    reg_form = RegistrationForm()

    # Update DB if validation success
    # Check if POST method was used and
    # if all validation was cleared
    if reg_form.validate_on_submit():
        # Obtain data from fields using flask wtform
        first_name = reg_form.first_name.data
        last_name = reg_form.last_name.data
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data

        # Hash plain text password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to database
        user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_pswd)

        db.session.add(user)
        db.session.commit()

        # Flash sends the message only once
        # Flash notification to user using bootstrap class
        flash('Registered succesfully. Please login.', 'success')

        # Redirect user to login page if successful registration
        return redirect(url_for('login'))

    # Display html
    return render_template("index.html", form=reg_form)

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success (no error)
    if login_form.validate_on_submit():

        # Get user object (email submitted in login form) from DB
        user_object = User.query.filter_by(email=login_form.email.data).first()
        # Load user to login
        login_user(user_object)
        # Redirect user to chat route
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)



@app.route("/chat", methods=['GET', 'POST'])
def chat():

    # User access protected chat page w/o logging in
    if not current_user.is_authenticated:
        # Error message to match bootstrap class
        flash('Please login.', 'danger')
        # Redirect to login page
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username)

# Route for logout
@app.route("/logout", methods=['GET'])
@login_required
def logout():

    logout_user()
    flash('You have logged out succesfully', 'success')
    # Redirect to login page
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# Create event handler/bucket
@socketio.on('message')
def message(data):
    """ Tell SocketIO what actions to take when clients send message to an event bucket """

    print(f"\n\n{data}\n\n")

    msg = data["msg"]
    username = data["username"]
    room = data["room"]

    sentiment = client.Sentiment({'text': msg})

    if sentiment['polarity'] == "positive":
        msg += " :)"
    elif sentiment['polarity'] == "negative":
        msg += " :("
    else:
        msg += " :|"

    global time_stamp

    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    time_stamp = time.strftime('%I:%M:%S %p', time.localtime())

    # Broadcast that new user has joined
    send({"msg": username + " joined at " + time_stamp}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)

    time_stamp = time.strftime('%I:%M:%S %p', time.localtime())

    send({"msg": username + " left at " + time_stamp}, room=room)

if __name__ == "__main__":

    # Start the server, restart server when file changed
    app.run(debug=True)
