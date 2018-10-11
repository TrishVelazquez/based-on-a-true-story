"""Based On A True Story Model Database"""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

###########################################################
# Model definitions #                                      
###########################################################


class User(db.Model):
    """User class"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Movie(db.Model):
    """Movie class"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(500), nullable=False)
    release_year = db.Column(db.Integer, nullable=True)
    plot = db.Column(db.String(500), nullable=False)
    poster = db.Column(db.String(500), nullable=False)
    website_url = db.Column(db.String(500), nullable=False)


class Truth(db.Model):
    """Truth Class"""

    __tablename__ = "truths"

    truth_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    truth_title = db.Column(db.String(100), nullable=False)
    truth_submission = db.Column(db.String(500), nullable=False)
    resource_submission = db.Column(db.String(500), nullable=True, default='N/A')
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # movie = db.relationship("Movie")

    # user = db.relationship("User")


class Rating(db.Model):
    """Truth Rating Class"""

    __tablename__ = "truth_ratings"

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    truth_id = db.Column(db.Integer, db.ForeignKey('truths.truth_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # truth = db.relationship("Truth")

###########################################################
# To be implemented in phase two. 

class Reply(db.Model):
    """Reply Class"""

    __tablename__ = "replies"

    reply_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    truth_id = db.Column(db.Integer, db.ForeignKey('truths.truth_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comment = db.Column(db.String(300), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # rating = db.relationship("Rating")


###########################################################
# Helper Functions #
###########################################################


def init_app():
    """Create a Flask app"""
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to Database.")


def connect_to_db(app):
    """Connect the database to Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///truestory'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    init_app()


