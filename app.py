import os

from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterUserForm, LoginUserForm, CSRFForm, NoteForm

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
    """Renders the home page."""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Handles the regristration of new users."""

    username = session.get("username")
    if username:
        return redirect(f"/users/{username}")

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email,
                             first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("registration-page.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Handles logging in for existing users."""

    username = session.get("username")
    if username:
        return redirect(f"/users/{username}")

    form = LoginUserForm()

    if form.validate_on_submit():

        username = form.username.data

        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            flash(message="Invalid login credentials")
            # form.username.errors = ["Bad username/password"]
            return redirect("/login")

    else:
        return render_template("login-page.html", form=form)


@app.get("/users/<string:username>")
def show_user(username):
    """Shows the user page for a logged-in user."""
# check session, if username route is not username session => redirect
#Go straight to conditionals instad of saving session_user
    session_user = session.get("username")
    if not session_user:
        return redirect("/login")

    if session_user != username:
        return redirect(f"/users/{session_user}")

    user = User.query.get_or_404(username)

    form = CSRFForm()

    if session_user == username:

        return render_template("user-page.html", user=user, form=form)


@app.post("/logout")
def logout_user():
    """Handles logging out a logged-in user."""

    form = CSRFForm()

    if form.validate_on_submit():
        session.pop("username", None)
        return redirect("/")

    return redirect("/")

@app.post('/users/<string:username>/delete')
def delete_user(username):
    """Deletes a user and their notes."""
    form = CSRFForm()
    session.pop("username", None)

    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        notes = user.notes
        for note in notes:
            db.session.delete(note)
            db.session.commit()

        db.session.delete(user)
        db.session.commit()

    return redirect("/")

@app.route('/users/<string:username>/notes/add', methods=["GET", "POST"])
def add_note(username):
    session_user = session.get("username")
    if not session_user:
        return redirect("/login")

    if session_user != username:
        return redirect(f"/users/{session_user}")

    form = NoteForm()

    if form.validate_on_submit():
        #is this query necessary?
        user = User.query.get_or_404(username)

        title = form.title.data
        content=form.content.data

        note = Note(title=title, content=content, owner_username=user.username)

        db.session.add(note)
        db.session.commit()
        return redirect(f"/users/{user.username}")

    else:
        return render_template("add-note-page.html", form=form)

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Updates a single note."""
    session_user = session.get("username")
    if not session_user:
        return redirect("/login")

    note = Note.query.get_or_404(note_id)

    if session_user != note.owner_username:
        return redirect(f"/users/{session_user}")

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()
        flash(message="Note updated")
        return redirect(f"/users/{session_user}")

    else:
        return render_template("edit-note-page.html", form=form)

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Deletes a single note."""
    session_user = session.get("username")
    if not session_user:
        return redirect("/login")

    note = Note.query.get_or_404(note_id)
    print("Note owner is:", note.owner_username)

    #Use note.oswner_username
    if (session_user != note.user.username):
        return redirect(f"/users/{session_user}")

    form = CSRFForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        flash(message="Note deleted")
        return redirect(f"/users/{session_user}")


    return redirect(f"/users/{session_user}")


