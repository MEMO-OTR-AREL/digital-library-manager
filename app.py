from flask import Flask, render_template, request, session, redirect
from book_data import BOOK_DATA
from database import create_tables, get_connection

app = Flask(__name__)
app.secret_key = "secret123"

create_tables()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
            """,
            (username, email, password)
        )

        connection.commit()
        connection.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
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


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )
    total_books = cursor.fetchone()[0]

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


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        status = request.form["status"]
        progress = request.form["progress"]

        if title not in BOOK_DATA:
            return redirect("/add_book")

        book = BOOK_DATA[title]

        connection = get_connection()
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
                cover_url,
                summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                book["author"],
                book["category"],
                status,
                book["rating"],
                progress,
                0,
                book["cover_url"],
                book["summary"]
            )
        )

        connection.commit()
        connection.close()

        return redirect("/books")

    return render_template("add_book.html")


@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search")
    category = request.args.get("category")
    status = request.args.get("status")
    favorite = request.args.get("favorite")
    top_rated = request.args.get("top_rated")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM books
        WHERE user_id = ?
    """

    parameters = [session["user_id"]]

    if category and category.strip() != "":
        query += " AND category = ?"
        parameters.append(category)

    if search and search.strip() != "":
        query += " AND title LIKE ?"
        parameters.append(f"%{search}%")

    if status and status.strip() != "":
        query += " AND status = ?"
        parameters.append(status)

    if favorite == "1":
        query += " AND favorite = 1"

    if top_rated == "1":
        query += " AND rating >= 9"

    query += " ORDER BY id DESC"

    cursor.execute(query, parameters)
    books = cursor.fetchall()

    connection.close()

    return render_template("books.html", books=books)



@app.route("/book/<int:book_id>")
def book_detail(book_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE id = ?
        AND user_id = ?
        """,
        (book_id, session["user_id"])
    )

    book = cursor.fetchone()
    connection.close()

    if book is None:
        return redirect("/books")

    return render_template("book_detail.html", book=book)


@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM books
        WHERE id = ?
        AND user_id = ?
        """,
        (book_id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return redirect("/books")


@app.route("/favorite_book/<int:book_id>")
def favorite_book(book_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE books
        SET favorite =
            CASE
                WHEN favorite = 1 THEN 0
                ELSE 1
            END
        WHERE id = ?
        AND user_id = ?
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

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        title = request.form["title"]
        status = request.form["status"]
        progress = request.form["progress"]

        if title not in BOOK_DATA:
            connection.close()
            return redirect("/books")

        book = BOOK_DATA[title]

        cursor.execute(
            """
            UPDATE books
            SET
                title = ?,
                author = ?,
                category = ?,
                status = ?,
                rating = ?,
                progress = ?,
                cover_url = ?,
                summary = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (
                title,
                book["author"],
                book["category"],
                status,
                book["rating"],
                progress,
                book["cover_url"],
                book["summary"],
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
        (book_id, session["user_id"])
    )

    book = cursor.fetchone()
    connection.close()

    if book is None:
        return redirect("/books")

    return render_template("edit_book.html", book=book)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)