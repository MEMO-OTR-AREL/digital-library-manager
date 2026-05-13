from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# HOME

@app.route("/")
def home():

    return render_template("home.html")


# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password)

            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                password
            )
        )

        connection.commit()
        connection.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ? AND password = ?
            """,
            (
                username,
                password
            )
        )

        user = cursor.fetchone()

        connection.close()

        if user:

            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# DASHBOARD

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # TOTAL BOOKS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )

    total_books = cursor.fetchone()[0]

    # READING BOOKS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE user_id = ?
        AND status = 'Reading'
        """,
        (session["user_id"],)
    )

    reading_books = cursor.fetchone()[0]

    # COMPLETED BOOKS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE user_id = ?
        AND status = 'Completed'
        """,
        (session["user_id"],)
    )

    completed_books = cursor.fetchone()[0]

    # FAVORITE BOOKS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE user_id = ?
        AND favorite = 1
        """,
        (session["user_id"],)
    )

    favorite_books = cursor.fetchone()[0]

    # RECENT BOOKS

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 3
        """,
        (session["user_id"],)
    )

    recent_books = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",

        username=session["username"],

        total_books=total_books,

        reading_books=reading_books,

        completed_books=completed_books,

        favorite_books=favorite_books,

        recent_books=recent_books
    )


# ADD BOOK

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

        # BOOK COVERS

        cover_map = {

            "Suç ve Ceza":
                "/static/images/suc_ve_ceza.jpg",

            "Kumarbaz":
                "/static/images/kumarbaz.jpg",

            "Sefiller":
                "/static/images/sefiller.jpg",

            "Clean Code":
                "/static/images/clean_code.jpg",

            "Python Crash Course":
                "/static/images/python_crash_course.jpg",

            "Atomic Habits":
                "/static/images/atomic_habits.jpg",

            "Thinking Fast and Slow":
                "/static/images/thinking_fast_and_slow.jpg",

            "Harry Potter":
                "/static/images/harry_potter.jpg",

            "Hobbit":
                "/static/images/hobbit.jpg",

            "Dune":
                "/static/images/dune.jpg"
        }

        cover_url = cover_map.get(
            title,
            "/static/images/suc_ve_ceza.jpg"
        )

        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO books
            (
                user_id,
                title,
                author,
                category,
                status,
                rating,
                progress,
                favorite,
                cover_url
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                author,
                category,
                status,
                rating,
                progress,
                0,
                cover_url
            )
        )

        connection.commit()
        connection.close()

        return redirect("/books")

    return render_template("add_book.html")


# BOOKS

@app.route("/books")
def books():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM books
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


# DELETE BOOK

@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM books
        WHERE id = ?
        AND user_id = ?
        """,
        (
            book_id,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    return redirect("/books")


# FAVORITE BOOK

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
        WHERE id = ?
        AND user_id = ?
        """,
        (
            book_id,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    return redirect("/books")


# EDIT BOOK

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

            SET
                title = ?,
                author = ?,
                category = ?,
                status = ?,
                rating = ?,
                progress = ?

            WHERE id = ?
            AND user_id = ?
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
        """
        SELECT *
        FROM books
        WHERE id = ?
        AND user_id = ?
        """,
        (
            book_id,
            session["user_id"]
        )
    )

    book = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_book.html",
        book=book
    )


# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)

