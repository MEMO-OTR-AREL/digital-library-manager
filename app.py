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

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM books WHERE user_id = ?",
        (session["user_id"],)
    )

    total_books = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*) FROM books
        WHERE user_id = ? AND status = 'Reading'
        """,
        (session["user_id"],)
    )

    reading_books = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*) FROM books
        WHERE user_id = ? AND status = 'Completed'
        """,
        (session["user_id"],)
    )

    completed_books = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        total_books=total_books,
        reading_books=reading_books,
        completed_books=completed_books
    )


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
        progress = request.form["progress"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO books
            (user_id, title, author, category, status, rating, progress)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                author,
                category,
                status,
                rating,
                progress
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

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    query = """
        SELECT * FROM books
        WHERE user_id = ?
    """

    parameters = [session["user_id"]]

    if search:
        query += " AND title LIKE ?"
        parameters.append(f"%{search}%")

    if category:
        query += " AND category = ?"
        parameters.append(category)

    cursor.execute(query, parameters)

    books = cursor.fetchall()

    connection.close()

    return render_template(
        "books.html",
        books=books
    )


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


@app.route("/favorite_book/<int:book_id>")
def favorite_book(book_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE books
        SET favorite = 1
        WHERE id = ? AND user_id = ?
        """,
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
        progress = request.form["progress"]

        cursor.execute(
            """
            UPDATE books
            SET title = ?, author = ?, category = ?, status = ?, rating = ?, progress = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                title,
                author,
                category,
                status,
                rating,
                progress,
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