from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


def create_database():
    connection = sqlite3.connect("library.db")

    with open("schema.sql", "r") as file:
        connection.executescript(file.read())

    connection.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        connection.commit()
        connection.close()

        return "User registered successfully!"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        user = cursor.fetchone()

        connection.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html", username=session["username"])


@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        status = request.form["status"]
        rating = request.form["rating"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO books
            (user_id, title, author, category, status, rating)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                author,
                category,
                status,
                rating
            )
        )

        connection.commit()
        connection.close()

        return "Book added successfully!"

    return render_template("add_book.html")


@app.route("/books")
def books():

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE user_id = ?",
        (session["user_id"],)
    )

    books = cursor.fetchall()

    connection.close()

    return render_template("books.html", books=books)


@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id = ? AND user_id = ?",
        (book_id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return redirect("/books")

@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        status = request.form["status"]
        rating = request.form["rating"]

        cursor.execute(
            """
            UPDATE books
            SET title = ?, author = ?, category = ?, status = ?, rating = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                title,
                author,
                category,
                status,
                rating,
                book_id,
                session["user_id"]
            )
        )

        connection.commit()
        connection.close()

        return redirect("/books")

    cursor.execute(
        "SELECT * FROM books WHERE id = ? AND user_id = ?",
        (book_id, session["user_id"])
    )

    book = cursor.fetchone()

    connection.close()

    return render_template("edit_book.html", book=book)

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)