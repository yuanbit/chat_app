from flask import Flask, render_template, redirect, url_for
from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uglcakesytydkw:a531b221acaeaf035634fb709b4bbe8d84995411718c1101104d7866fdfcdc70@ec2-174-129-33-201.compute-1.amazonaws.com:5432/d1jr4qvs8g9vgl'

db = SQLAlchemy(app)

# Route for homepage/registration page
@app.route("/", methods=['GET', 'POST'])
# Renders the fields
def index():

    reg_form = RegistrationForm()

    # Update DB if validation success
    # Check if POST method was used and
    # if all validation was cleared
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Add user to database
        user = User(username=username, password=password)
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

        # Return a post login page
        return "Loggin in, finally!"

    return render_template("login.html", form=login_form)


if __name__ == "__main__":

    # Run in debug method, don't have to re-start server
    app.run(debug=True)
