import os

from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
#from forms import RegisterUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def show_homepage():
    return redirect("/register")

@app.route("/register", methods= ["GET", "POST"])
def register_user():

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name= form.last_name.data

        user = User.register(username=username, password=password, email=email,
                             first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("registration-page.html", form=form)