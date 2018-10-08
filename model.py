"""Based On A True Story Model Database"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

###########################################################
# Model difinitions

class User(db.Model):
    """User class"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Movie(db.Model):
    """Movie class"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    plot = db.Column(db.String(500), nullable=False)
    poster = db.Column(db.String(300), nullable=True)
    true_story = db.Column(db.Integer, nullable=True)
    amazon_url = db.Column(db.String(300), nullable=True)


class Truth(db.Model):
    """Truth Class"""

    __tablename__ = "truths"

    truth_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    truth_submission = db.Column(db.String(500), nullable=False)
    resource_submission = db.Column(db.String(500), nullable=True)


    movie = db.relationship("Movie",
                            backref=db.backref("truths",
                            order_by=truth_id))

    user = db.relationship("User",
                            backref=db.backref("truths",
                            order_by=truth_id))


class Rating(db.Model):
    """Truth Rating Class"""

    __tablename__ = "truth_ratings"

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    truth_id = db.Column(db.Integer, db.ForeignKey('truths.truth_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    rating = db.Column(db.Integer, nullable=True)


    truth = db.relationship("Truth",
                            backref=db.backref("truth_ratings",
                            order_by=rating_id))

    user = db.relationship("User",
                            backref=db.backref("truth_ratings",
                            order_by=rating_id))







