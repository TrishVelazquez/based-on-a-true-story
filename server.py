
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

    user_info = db.session.query(User.username, User.email, User.password).all()

    for user in user_info:
        if user[1] == email and user[2] == password:
            
            flash(u"Logged in. Welcome back, " + user[0])
            session["active_user"] = user[0]

            return redirect("/")

        else:
            continue 

    flash(u"No account found for the entered email/password. Please try again.")
    return render_template("login_account.html")


@app.route('/logout')
def logout():
    """Log out."""

    del session["active_user"]
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
def find_movies():
    """Search for movies through oMDB API"""

    movies_in_database = db.session.query(Movie.title).all()

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

    elif "Biography" in data['Genre']:
        for each_movie in movies_in_database:
            if data['Title'] != ''.join(each_movie): 
                print(data['Title'])
                print(''.join(each_movie))
                print("\n\n\n\n")

                # Currently adding too many to database. Will fix. 

                new_movie= Movie(title=data['Title'],
                                genre=data['Genre'],
                                year=data['Year'],
                                plot=data['Plot'],
                                poster=data['Poster'],
                                website_url=data['Website'])

        db.session.add(new_movie)
        db.session.commit()
        
        return render_template("search_results.html",
                                data=pformat(data),
                                title = data['Title'],
                                year = data['Year'],
                                genre = data['Genre'],
                                plot = data['Plot'],
                                poster = data['Poster'],
                                website_url = data['Website'])

    else:

        return render_template("search_results.html",
                                data=pformat(data),
                                title = data['Title'],
                                year = data['Year'],
                                genre = data['Genre'],
                                plot = data['Plot'],
                                poster = data['Poster'],
                                website_url = data['Website'])




# @app.route('/add-new-movie', methods=["POST"])
# def add_movie_to_database():

#     title = request.form.get("movie-title")
#     year = request.form.get("release-year")
#     genre = request.form.get("genre")
#     plot = request.form.get("plot")
#     poster = request.form.get("poster")
#     website_url = request.form.get("website")

#     movie_titles = Movie.query.filter_by(title=title).all()
#     print(title)
#     print("\n\n\n\n\n\n")

#     for one_title in movie_titles:

#         if title == one_title:

#             return redirect("/")

#         else:

#             new_movie = Movie(title=title, 
#                             genre=genre, 
#                             year=year,
#                             plot=plot, 
#                             poster=poster, 
#                             website_url=website_url)
#             db.session.add(new_movie)
#             db.session.commit()

#             return render_template("movie_info.html")


@app.route("/movies")
def show_all_movies_in_database():
    """Show all the movies currently in the database."""

    movies = Movie.query.order_by('title').all()
    return render_template("movie_list.html", movies=movies)

            

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

