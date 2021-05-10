from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """Users"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    residentState = db.Column(
        db.Text,
        nullable=False,        
    )

    residentCity = db.Column(
        db.Text,
        nullable=False,    
    )

    residentStreetAddress = db.Column(
        db.Text,
        nullable=False,
    )

    residentZipCode = db.Column(
        db.Integer,
        nullable=False,
        )

    def __init__(self, username, password, email, residentState, residentCity, residentStreetAddress, residentZipCode):
        self.username = username
        self.password = password
        self.email = email 
        self.residentState = residentState
        self.residentCity = residentCity
        self.residentStreetAddress = residentStreetAddress
        self.residentZipCode = residentZipCode

    @classmethod
    def signup(cls, username, password, email, residentState, residentCity, residentStreetAddress, residentZipCode):
        """Register user and hashes password."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            residentState=residentState,
            residentCity=residentCity,
            residentStreetAddress=residentStreetAddress,
            residentZipCode=residentZipCode,
        )

        db.session.add(user)
        return username, residentState
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
    

