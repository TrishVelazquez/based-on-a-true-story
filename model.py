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
    title = db.Column(db.String(600), nullable=False)
    genre = db.Column(db.String(600), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    plot = db.Column(db.String(600), nullable=False)
    poster = db.Column(db.String(600), nullable=False)
    website_url = db.Column(db.String(600), nullable=False)



class Truth(db.Model):
    """Truth Class"""

    __tablename__ = "truths"

    truth_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    truth_title = db.Column(db.String(100), nullable=False)
    truth_submission = db.Column(db.String(600), nullable=False)
    resource_submission = db.Column(db.String(600), nullable=True, default='N/A')
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)



class Rating(db.Model):
    """Truth Rating Class"""

    __tablename__ = "truth_ratings"

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    truth_id = db.Column(db.Integer, db.ForeignKey('truths.truth_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)


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
    username = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    comment = db.Column(db.String(300), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)


###########################################################
# Example Data #
###########################################################


def example_data():
    """Create sample data for tests"""

    user1 = User(username="filmbuff",
                email="films@yahoo.com",
                password="films")

    user2 = User(username="movies4ever",
                email="123@gmail.com",
                password="123")

    movie1 = Movie(title="BlacKkKlansman",
                genre="Biography, Comedy, Crime, Drama",
                year="2018",
                plot="Ron Stallworth, an African American police officer from Colorado Springs, CO, successfully manages to infiltrate the local Ku Klux Klan branch with the help of a Jewish surrogate who eventually becomes its leader. Based on actual events.",
                poster="https://m.media-amazon.com/images/M/MV5BMjUyOTE1NjI0OF5BMl5BanBnXkFtZTgwMTM4ODQ5NTM@._V1_SX300.jpg",
                website_url="N/A")

    movie2 = Movie(title="127 Hours",
                genre="Adventure, Biography, Drama",
                year="2010",
                plot="An adventurous mountain climber becomes trapped under a boulder while canyoneering alone near Moab, Utah and resorts to desperate measures in order to survive.",
                poster="https://m.media-amazon.com/images/M/MV5BMTc2NjMzOTE3Ml5BMl5BanBnXkFtZTcwMDE0OTc5Mw@@._V1_SX300.jpg",
                website_url="http://www.127hoursmovie.com/")

    movie3 = Movie(title="Beetlejuice",
                genre="Comedy, Fantasy",
                year="1998",
                plot="A recently-deceased husband and wife commission a bizarre demon to drive an obnoxious family out of their home.",
                poster="https://m.media-amazon.com/images/M/MV5BZDdmNjBlYTctNWU0MC00ODQxLWEzNDQtZGY1NmRhYjNmNDczXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
                website_url="N/A")

    truth1 = Truth(movie_id=1,
                user_id=1,
                username="filmbuff",
                truth_title="A Truth",
                truth_submission="Something about this movie.",
                resource_submission="www.this.com")

    truth2 = Truth(movie_id=2,
                user_id=2,
                username="movies4ever",
                truth_title="A Thing",
                truth_submission="A fun fact for you.")


    # import pdb
    # pdb.set_trace()

    db.session.add_all([user1, user2, movie1, movie2, movie3])
    db.session.commit()

    db.session.add_all([truth1, truth2])
    db.session.commit()



###########################################################
# Helper Functions #
###########################################################


def init_app():
    """Create a Flask app"""
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to Database.")


def connect_to_db(app, db_uri="postgresql:///testdb"):
    """Connect the database to Flask app"""

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///truestory'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    init_app()


