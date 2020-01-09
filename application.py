from flask import Flask, render_template
from wtform_fields import *

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])

# Each time a user visits the page
def index():

    reg_form = RegistrationForm()
    # Check if POST method was used and
    # if all validation was cleared
    if reg_form.validate_on_submit():
        return 'Great success!'

    # Display html
    return render_template("index.html", form=reg_form)

if __name__ == "__main__":

    # Run in debug method, don't have to re-start server
    app.run(debug=True)
