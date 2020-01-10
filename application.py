from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uglcakesytydkw:a531b221acaeaf035634fb709b4bbe8d84995411718c1101104d7866fdfcdc70@ec2-174-129-33-201.compute-1.amazonaws.com:5432/d1jr4qvs8g9vgl'

db = SQLAlchemy(app)

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
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash plain text password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        # Take user to login page if successful registration
        return redirect(url_for('login'))

    # Display html
    return render_template("index.html", form=reg_form)

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success (no error)
    if login_form.validate_on_submit():

        # Get user object (username submitted in login form) from DB
        user_object = User.query.filter_by(username=login_form.username.data).first()
        # Load user to login
        login_user(user_object)
        # Redirect user to chat route
        return redirect(url_for('chat'))
        # If current user is logged in
        # if current_user.is_authenticated:
            # Return a post login page
            # return "Loggin in with flask-login!"
        #return "Not logged in!"

    return render_template("login.html", form=login_form)

# Route (protected) for chat application page - only a logged in user can view
@app.route("/chat", methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        # Return a post login page
        return "Please login before accessing chat"
    return "Chat with me"

# Route for logout
@app.route("/logout", methods=['GET'])
#@login_required
def logout():

    logout_user()

    return "Logged out using flask_login"


if __name__ == "__main__":

    # Run in debug method, don't have to re-start server
    app.run(debug=True)
