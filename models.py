"""Models for Notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model."""
    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        unique=True,
        primary_key=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Creates a new user instance to be registered and saved in the
        database."""
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed, email=email,
                   first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
    Return user if valid; else return False.
    """
        u = cls.query.filter_by(username=username).one_or_none()
        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u

        else:
            return False

