from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from db import User

def invalid_credentials(form, field):
    """ Email and password checker """

    # Check if username and password are valid
    email_entered = form.email.data
    password_entered = field.data

    # Check if username exist in DB
    user_object = User.query.filter_by(email=email_entered).first()
    # If username doesn't exist
    if user_object is None:
        raise ValidationError("Email or password is incorrect.")
    # Check if password matches password in DB
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Email or password is incorrect.")


class RegistrationForm(FlaskForm):
    """ Registration form """

    # Define fields for the registration form
    # Adds input tags in html
    first_name = StringField('first_name_label', validators=[InputRequired(message="First name required."), Length(max=100, message="First name must be less than 100 characters.")])

    last_name = StringField('last_name_label', validators=[InputRequired(message="Last name required."), Length(max=100, message="Last name must be less than 100 characters.")])

    username = StringField('username_label', validators=[InputRequired(message="Username required."), Length(min=4, max=25, message="Username must be between 4 and 25 characters.")])

    email = StringField('email_label', validators=[InputRequired(message="Email required."), Length(max=100, message="Email must be under 100 characters.")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password required."), Length(min=4, max=25, message="Password must be between 4 and 25 characters.")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Password required."), EqualTo('password', message="Passwords don't match.")])

    submit_button = SubmitField('Register')

    def validate_username(self, username):
        """ Username duplicate checker """
        # Get username from DB
        user_object = User.query.filter_by(username=username.data).first()

        # If username exists
        if user_object:
            raise ValidationError("Username is already registered. Please use a different username.")

    def validate_email(self, email):
        """ Email duplicate checker """

        # Get email from DB
        user_object = User.query.filter_by(email=email.data).first()
        # If email exists
        if user_object:
            raise ValidationError("Email is already registered. Please use a different email.")


class LoginForm(FlaskForm):
    """ Login form """

    email = StringField('email_label', validators=[InputRequired(message="Email required.")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password required."), invalid_credentials])

    submit_button = SubmitField('Login')
