
###########################################################
# Based On A True Story Server #
###########################################################

from pprint import pformat
import os
import requests

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Movie, Truth, Rating, Reply, connect_to_db, db 


app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


###########################################################
# Routes #
###########################################################

@app.route('/')
def homepage():
    """Take user to the homepage"""

    return render_template("homepage.html")


@app.route('/login')
def login_route():
    """Take user to the login screen"""

    return render_template("login_account.html")


@app.route('/login-verify', methods =["POST"])
def user_login():
    """Verify user exists in database"""

    email = request.form.get('user_email')
    password = request.form.get('user_password')

    user_info = db.session.query(User.username, User.email, User.password, User.user_id).all()

    for user in user_info:
        if user[1] == email and user[2] == password:
            
            flash(u"Logged in. Welcome back, " + user[0])
            session["active_user"] = user[0]
            session["active_user_id"] = user[3]

            return redirect("/")

        else:
            continue 

    flash(u"No account found for the entered email/password. Please try again.")
    return render_template("login_account.html")


@app.route('/logout')
def logout():
    """Log out."""

    del session["active_user"]
    del session["active_user_id"]

    flash(u"You've been logged out.")
    return redirect("/")


@app.route('/create-account')
def create_new_user():
    """Create a new user account"""

    return render_template("create_account.html")


@app.route('/process-account', methods =["POST"])
def process_new_user():
    """Process new user account"""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user_info = User.query.filter_by(email=email).all()

    if user_info:
        flash(u"You already have an account! Please log in.")
        return redirect("/login")

    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template("homepage.html")


@app.route('/search-results')
def find_and_add_movies():
    """Search for movies from the oMDB API & add them to database."""

    query = request.args.get('query')
    url = 'http://www.omdbapi.com/'
    payload = {
        'apikey' : os.environ["OMDB_KEY"],
        't' : query
    }

    """Query API with the results from the searchbar"""

    response = requests.get(url, params=payload)
    data = response.json()

    """Save json response in data object"""


    if data == {'Response': 'False', 'Error': 'Movie not found!'}:

        flash(u"Oops, that's not a movie title. Please try again.")
        return redirect("/")


    """If data response is an error (any incorrect search raises this error) redirect to homepage"""

    if "History" in data['Genre'] or "Biography" in data['Genre']:
        movie_title = Movie.query.filter_by(title=data['Title']).all()
        if not movie_title:
        # print("I'm adding the movie to the database! \n")

            new_movie= Movie(title=data['Title'],
                            genre=data['Genre'],
                            year=data['Year'],
                            plot=data['Plot'],
                            poster=data['Poster'],
                            website_url=data['Website'])

            db.session.add(new_movie)
            db.session.commit()


    """If a movie that has the terms History or Biography 
    in its genre is not in the database, add it"""


    # print("Displaying stuff!\n")
    movies = Movie.query.order_by('title').all()
    return render_template("search_results.html",
                                movies=movies,
                                title = data['Title'],
                                year = data['Year'],
                                genre = data['Genre'],
                                plot = data['Plot'],
                                poster = data['Poster'],
                                website_url = data['Website'])


@app.route("/movie-list")
def show_movies_list():
    """Show all of the movies currently in the database"""

    movies = Movie.query.order_by('title').all()
    return render_template("movie_list.html",
                            movies=movies)



@app.route("/movies/<int:movie_id>", methods=["GET"])
def show_movie_info(movie_id):
    """Show a single movie in the database and all Truths associated with it.
    Show fields to add Truths for registered users."""

    movie = Movie.query.get(movie_id)

    # user_id = session.get("active_user_id")
    users = User.query.order_by('user_id').all

    movie_truths = Truth.query.filter_by(movie_id=movie_id).all()

    return render_template("movie_info.html",
                            # user_id=user_id,
                            users=users,
                            movie=movie,
                            movie_truths=movie_truths)



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




###########################################################

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

