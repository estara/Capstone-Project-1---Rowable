"""Models for Rowable app"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()


class Boathouse(db.Model):
    """Boathouse"""
    __tablename__ = 'boathouse'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    state = db.Column(db.Text, nullable=True)
    zip = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Numeric, nullable=True)
    lon = db.Column(db.Numeric, nullable=True)
    notes = db.Column(db.Text)
    activated = db.Column(db.Boolean, default=False)
    nmax = db.Column(db.Integer, nullable=True)
    smax = db.Column(db.Integer, nullable=True)
    emax = db.Column(db.Integer, nullable=True)
    wmax = db.Column(db.Integer, nullable=True)
    fun_limit = db.Column(db.Integer, nullable=True)
    users = db.relationship('User')


class User(db.Model):
    """User"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=True)
    hashed_password = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=True)
    c_or_f = db.Column(db.Text, default='imperial', nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    boathouses = db.Column(db.Integer, db.ForeignKey('boathouse.id'))

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            hashed_password=hashed_pwd,
            email=email,
            registered_on=datetime.now()
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates user for login"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.hashed_password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
