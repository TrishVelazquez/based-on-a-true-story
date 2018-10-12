
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

    email = request.args.get("email")
    password = request.args.get("password")
    user_info = db.session.query(User.username, User.email, User.password).all()

    for user in user_info:
        if user.email == email and user.password == password:
            session["active_user"] = user.username
            flash(u"Logged in. Welcome back, " + user.username)

            return redirect("/")

        else:
            continue 

    flash(u"No account found for the entered email/password. Please try again.")
    return render_template("login_account.html")


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
        print("You already have an account! Please log in.")

    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template("homepage.html")


@app.route('/search-results')
def find_movies():
    """Search for movies through oMDB API"""

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

    else:

        return render_template("search_results.html",
                                data=pformat(data),
                                title = data['Title'],
                                genre = data['Genre'],
                                release_year = data['Released'],
                                plot = data['Plot'],
                                poster = data['Poster'],
                                website_url = data['Website'])


# @app.route('/add-new-movie', methods=["POST"])
# def add_moive_to_database():

#     title = 
#     genre = 
#     release_year = 
#     plot = 
#     poster = 
#     website_url = 


# @app.route('/add-new-movie-fact', methods=["POST"])
# def add_movie_truths():

    
#     user = session["active_user"]
#     title = request.form.get("title")
#     submission = request.form.get("truth")
#     resource = request.form.get("resource")

#     new_truth = Truth(truth_title=title, truth_submission=truth, truth_resource=resource)
#     db.session.add(new_truth)
#     db.session.commit()

#     return render_template("")




###########################################################

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

