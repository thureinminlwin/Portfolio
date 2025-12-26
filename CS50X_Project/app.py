import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show the table of decks"""

    # find the decks in the deck table for currently logged in user and show it in home page.
    decks = db.execute("SELECT * FROM decks WHERE user_id = ?", session["user_id"])
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    return render_template("index.html", decks=decks, user=user[0])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username is submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure the password was submitted
        elif not password or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # Check if the passwords match
        if password != request.form.get("confirmation"):
            return apology("The passwords do not match!")

        # Check if the username already exists.
        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return apology("The username already exists!")

        # Add the username and password into the database
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)",
                   username, generate_password_hash(password))

        row = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))
        session["user_id"] = row[0]["id"]

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/create_deck", methods=["GET", "POST"])
@login_required
def create_deck():
    """Allow the user to create a new deck (pack)"""

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        # Validate inputs
        if not name:
            return apology("Missing name!")
        if not description:
            return apology("Missing description!")

        # Add new decks into the database
        db.execute("INSERT INTO decks (user_id,name,description) VALUES (?,?,?)",
                   session["user_id"], name, description)

        return redirect("/")
    else:
        return render_template("create_deck.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Allows users to add words"""

    if request.method == "POST":
        word = request.form.get("word")
        meaning = request.form.get("meaning")
        example = request.form.get("example")
        deck_id = request.form.get("deck_id")

        # Validate inputs
        if not word:
            return apology("Missing word!")
        if not meaning:
            return apology("Missing meaning!")
        if not example:
            return apology("Missing example!")

        # Insert words into the database
        db.execute("INSERT INTO words (user_id,deck_id,word,meaning,example) VALUES(?,?,?,?,?)",
                   session["user_id"], deck_id, word, meaning, example)

        flash("Word added successfully!")

        # Show the view page
        return redirect(f"/view?deck_id={deck_id}")
    else:
        deck_id = request.args.get("deck_id")
        return render_template("add.html", deck_id=deck_id)


@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    """Allow the user to view the words in the deck"""
    if request.method == "GET":
        deck_id = request.args.get("deck_id")

        # Get the words with the deck_id
        table = db.execute("SELECT * FROM words WHERE deck_id = ?", deck_id)
        deck_name = db.execute("SELECT name FROM decks WHERE id = ?", deck_id)
        return render_template("view.html", table=table, deck_name=deck_name, deck_id=deck_id)


@app.route("/edit_deck", methods=["GET", "POST"])
@login_required
def edit_deck():
    """Allow the user to edit the deck"""
    if request.method == "POST":
        deck_id = request.form.get("deck_id")
        new_name = request.form.get("name")

        # Validate new inputs
        if not new_name:
            return apology("Missing name!")
        new_description = request.form.get("description")
        if not new_description:
            return apology("Missing description!")

        # Update the deck in the database
        db.execute("UPDATE decks SET name = ?, description = ? WHERE id = ? AND user_id = ?",
                   new_name, new_description, deck_id, session["user_id"])
        return redirect("/")

    else:
        # Get the deck_id to display the words in the deck
        deck_id = request.args.get("deck_id")
        deck = db.execute("SELECT * FROM decks WHERE id = ? AND user_id = ?",
                          deck_id, session["user_id"])
        return render_template("edit_deck.html", deck=deck[0])


@app.route("/edit_word", methods=["GET", "POST"])
@login_required
def edit_word():
    """Allow the user to edit the words in the deck"""
    if request.method == "POST":

        # Get inputs
        word_id = request.form.get("word_id")
        new_word = request.form.get("word")
        new_meaning = request.form.get("meaning")
        new_example = request.form.get("example")
        deck_id = request.form.get("deck_id")

        # Validate inputs
        if not new_word or not new_meaning or not new_example:
            return apology("Fill all the required inputs!")

        # Update the word in the words table
        db.execute("UPDATE words SET word = ?, meaning = ?, example = ? WHERE id = ? AND user_id = ?",
                   new_word, new_meaning, new_example, word_id, session["user_id"])

        return redirect(f"/view?deck_id={deck_id}")
    else:
        # Get the id of the word from index and pass it when rendering add page
        word_id = request.args.get("word_id")
        word = db.execute("SELECT * FROM words WHERE id = ? AND user_id = ?",
                          word_id, session["user_id"])
        return render_template("edit_word.html", word=word[0])


@app.route("/delete_word", methods=["POST"])
@login_required
def delete_word():
    """Allow the user to delete word"""
    word_id = request.form.get("word_id")
    deck_id = request.form.get("deck_id")
    db.execute("DELETE FROM words WHERE id = ? AND user_id = ?", word_id, session["user_id"])
    return redirect(f"/view?deck_id={deck_id}")


@app.route("/delete_deck", methods=["POST"])
@login_required
def delete_deck():
    """Allow the user to delete an entire deck of words"""
    deck_id = request.form.get("deck_id")

    # First, delete all words in that deck
    db.execute("DELETE FROM words WHERE deck_id = ? AND user_id = ?", deck_id, session["user_id"])

    # Then, delete the deck itself
    db.execute("DELETE FROM decks WHERE id = ? AND user_id = ?", deck_id, session["user_id"])

    return redirect("/")
