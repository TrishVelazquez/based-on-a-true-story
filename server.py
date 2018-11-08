
################################################################
# Based On A True Story Server #
################################################################

from pprint import pformat
import os
import requests

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Movie, Truth, Rating, Reply, connect_to_db, db 

app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


app.secret_key = os.environ["SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


################################################################
# Routes #
################################################################

@app.route('/')
def homepage():
    """Take the user to the homepage"""

    return render_template("homepage.html")


################################################################

@app.route('/create-account')
def create_new_user():
    """Create a new account for a user"""

    return render_template("create_account.html")


################################################################

@app.route('/process-account', methods =["POST"])
def process_new_user():
    """Process a new account"""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    registered_email = User.query.filter_by(email=email).all()
    registered_username = User.query.filter_by(username=username).all()

    if registered_email:
        flash(u"Your email is already registerd. Please log in.")
        return redirect("/login")

    if registered_username:
        flash(u"That username is taken! Please try another.")
        return redirect("/create-account")

    else:
        new_user = User(username=username, 
                        email=email, 
                        password=password)

        db.session.add(new_user)
        db.session.commit()

        flash(u"Your account has been created! Please log in.")
        return redirect("/login")


################################################################

@app.route('/login')
def login_route():
    """Take user to the login screen"""

    return render_template("login_account.html")


################################################################

@app.route('/login-verify', methods =["POST"])
def user_login():
    """Verify user exists in database"""

    email = request.form.get('email')
    password = request.form.get('password')

    all_users = User.query.order_by('user_id').all()

    for user in all_users:

        if user.email == email and user.password == password:

            flash(u"Logged in. Welcome back, " + user.username)
            session["active_user"] = user.username
            session["active_user_id"] = user.user_id

            return redirect("/")

    flash(u"Incorrect email and/or password. Please try again.")
    return render_template("login_account.html")


################################################################

@app.route('/logout')
def logout():
    """Log out."""

    del session["active_user"]
    del session["active_user_id"]

    flash(u"You've been logged out. We'll miss you.")
    return redirect("/")


################################################################

@app.route('/search-results')
def find_and_add_movies():
    """Search for movies from the oMDB API & add them to database."""

    query = request.args.get('query')
    url = 'http://www.omdbapi.com/'
    payload = {
        'apikey' : os.environ["OMDB_KEY"],
        't' : query
        }

    response = requests.get(url, params=payload)
    data = response.json()

    if data == {'Response': 'False', 'Error': 'Movie not found!'}:

        flash(u"Oops, that's not a movie title. Please try again.")
        return redirect("/")

    if "History" in data['Genre'] or "Biography" in data['Genre']:
        movie_title = Movie.query.filter_by(title=data['Title']).all()

        if not movie_title:

            new_movie= Movie(title=data['Title'],
                                genre=data['Genre'],
                                year=data['Year'],
                                plot=data['Plot'],
                                poster=data['Poster'],
                                website_url=data['Website'])

            db.session.add(new_movie)
            db.session.commit()

    movies = Movie.query.order_by('title').all()
    return render_template("search_results.html",
                                movies=movies,
                                title = data['Title'],
                                year = data['Year'],
                                genre = data['Genre'],
                                plot = data['Plot'],
                                poster = data['Poster'],
                                website_url = data['Website'])


################################################################

@app.route("/movie-list")
def show_movies_list():
    """Show all of the movies currently in the database"""

    movies = Movie.query.order_by('title').all()
    return render_template("movie_list.html",
                            movies=movies)


################################################################

@app.route("/movies/<int:movie_id>", methods=["GET"])
def show_movie_info(movie_id):
    """Show a single movie in the database and all Truths associated with it.
    Show fields to add Truths for registered users."""

    movie = Movie.query.get(movie_id)
    users = User.query.order_by('user_id').all
    movie_truths = Truth.query.filter_by(movie_id=movie_id).all()
    replies = Reply.query.filter_by(movie_id=movie_id).all()

    return render_template("movie_info_message_board.html",
                            users=users,
                            movie=movie,
                            movie_truths=movie_truths,
                            replies=replies)


################################################################

@app.route("/movies/<int:movie_id>", methods=["POST"])
def add_truth_to_movie(movie_id):
    """Let account holders add their Truths to a movie"""

    username = session.get("active_user")
    user_id = session.get("active_user_id")
    title = request.form.get("title")
    truth = request.form.get("truth")
    resource = request.form.get("resource")

    new_truth = Truth(movie_id=movie_id, 
                        user_id=user_id,
                        username=username, 
                        truth_title=title, 
                        truth_submission=truth, 
                        resource_submission=resource)

    db.session.add(new_truth)
    db.session.commit()

    flash(u"Your truth has been submitted!")
    return redirect(f"/movies/{movie_id}")


################################################################

@app.route("/add-reply", methods=["POST"])
def add_reply_to_truth():
    """Add replies to submitted truths"""

    username = session.get("active_user")
    user_id = session.get("active_user_id")
    movie_id = request.form.get("movie_id")
    truth_id = request.form.get("truth_id")
    comment = request.form.get("comment")

    new_reply = Reply(truth_id=truth_id,
                        movie_id=movie_id,
                        user_id=user_id,
                        username=username,
                        comment=comment)

    db.session.add(new_reply)
    db.session.commit()

    flash(u"Posted!")
    return redirect(f"/movies/{movie_id}")


################################################################

@app.route("/user/<int:user_id>")
def user_details(user_id):
    """Show info about the user and their activity"""
    
    user = User.query.get(user_id)
    movies = Movie.query.all()
    user_truths = Truth.query.filter_by(user_id=user_id).all()
    user_replies = Reply.query.filter_by(user_id=user_id).all()


    return render_template("user.html",
                            movies=movies,
                            user=user,
                            user_truths=user_truths,
                            user_replies=user_replies)


################################################################

@app.route("/process-vote")
def process_vote():
    """Processes an upvote or downvote to the database"""

    new_vote = Rating(truth_id=truth_id,
                        user_id=user_id,
                        username=username,
                        rating=rating)

    db.session.add(new_vote)
    db.session.commit()

    return redirect(f"/movie/{movie.id}")


################################################################

################################################################

if __name__ == "__main__":

    app.debug = False
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, db_uri="postgresql:///truestory")

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

