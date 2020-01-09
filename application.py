from flask import Flask, render_template
from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uglcakesytydkw:a531b221acaeaf035634fb709b4bbe8d84995411718c1101104d7866fdfcdc70@ec2-174-129-33-201.compute-1.amazonaws.com:5432/d1jr4qvs8g9vgl'

db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
# Renders the fields
def index():

    reg_form = RegistrationForm()
    # Check if POST method was used and
    # if all validation was cleared
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists
        # Database already has a constraint of unique username in column
        user_object = User.query.filter_by(username=username).first()

        # Check username duplicate
        if user_object:

            return "Someone else has taken this username!"
        # Get username associated with user
        # user_object.username

        # Add user to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return "Inserted into DB!"

    # Display html
    return render_template("index.html", form=reg_form)

if __name__ == "__main__":

    # Run in debug method, don't have to re-start server
    app.run(debug=True)
