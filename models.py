from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """ User model - define users

    UserMixin - tells flask_login about user
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # Max len = 25, no duplicate usernames, not empty
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
