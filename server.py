
###########################################################
# Based On A True Story Server #
###########################################################

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Movie, Truth, Rating, Reply, connect_to_db, db 

app = Flask(__name__)

app.secret_key = "SOSECRET"

app.jinja_env.undefined = StrictUndefined


###########################################################
# Routes #
###########################################################

@app.route('/')
def homepage():
    """Take user to the homepage"""

    return render_template("homepage.html")

###########################################################

@app.route('/login')
def login_route():
    """Take user to the login screen"""

    return render_template("login_account.html")

###########################################################

@app.route('/login-verify')
def user_login():
    """Verify user exists in database"""

    email = request.args.get("email")
    password = request.args.get("password")
    user_info = db.session.query(User.username, User.email, User.password).all()

    for user in user_info:
        if user.email == email and user.password == password:
            flash(u"Logged in. Welcome back, " + user.username)
            session["active_user"] = user.username

            return redirect("/")

        else:
            continue 

    flash(u"No account found for the entered email/password. Please try again.")
    return render_template("login_account.html")

###########################################################

@app.route('/create-account')
def create_new_user():
    """Create a new user account"""

    return render_template("create_account.html")

###########################################################

@app.route('/process-account', methods =["POST"])
def process_new_user():
    """Process new user account"""

    email = request.form.get("email")
    password = request.form.get("password")

    user_info = User.query.filter_by(email=email).all()

    if user_info:
        print("")

    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template("homepage.html")

###########################################################

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

