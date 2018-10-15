"""Utility file to seed sample data to model.py"""

import datetime
from sqlalchemy import func
from model import User
from model import Movie
from model import Truth
from model import Rating
# from model import Reply
from model import connect_to_db, db 
from server import app

###########################################################

def load_users():
    """Load sample users to user table"""

    print("Users")

    User.query.delete()

    for row in open("seed_data/u.user"):

        row = row.rstrip()

        user_id, username, email, password = row.split("|")

        user = User(user_id=user_id,
                    username=username,
                    email=email,
                    password=password)

        db.session.add(user)
    db.session.commit()



def load_movies():
    """Load sample movies to movie table"""

    print("Movies")

    Movie.query.delete()

    for movie in open("seed_data/u.movie"):

        movie = movie.rstrip()

        title, genre, plot, poster, website_url = movie.split("|")

        movie = Movie(title=title,
                    genre=genre,
                    plot=plot,
                    poster=poster,
                    website_url=website_url)

        db.session.add(movie)
    db.session.commit()



def load_truth():
    """Load sample truths to truth table"""

    print("Truths")

    Movie.query.delete()

    for row in open("seed_data/u.truth"):

        row = row.rstrip()

        truth_id, movie, user, title, submission, resource = row.split("|")

        truth = Truth(truth_id=truth_id,
                        movie_id=movie,
                        user_id=user,
                        truth_title=title,
                        truth_submission=submission,
                        truth_resource=resource)

        db.session.add(truth)
    db.session.commit()



def load_rating():
    """Load sample ratings to truth_ratings table"""

    print("Ratings")

    Rating.query.delete()

    for row in open("seed_data/u.rating"):

        row = row.rstrip()

        rating_id, truth_id, user_id, rating = row.split("|")

        rating = Rating(rating_id=rating_id,
                        truth_id=truth_id,
                        user_id=user_id,
                        rating=rating)

        db.session.add(rating)
    db.session.commit()
    

###########################################################
# To be implemented in phase two. 

# def load_reply():
#     """Load sample replies to truth_ratings table"""

#     print("Replies")

#     Reply.query.delete()

#     for row in open("seed_data/u.reply"):

#         row = row.rstrip()

#         reply_id, truth_id, user_id, comment = row.split("|")

#         reply = Rating(reply_id=reply_id,
#                         truth_id=truth_id,
#                         user_id=user_id,
#                         comment=comment)

#         db.session.add(reply)
#     db.session.commit()

###########################################################
# Helper Functions
###########################################################


def set_val_user_id():
    """Set value for the next user_id after seeding the database"""

    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id: max_id + 1'})
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_users()
    load_movies()
    load_truth()
    load_rating()
    # load_reply()






