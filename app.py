from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


BOOK_DATA = {
    "Crime and Punishment": {
        "author": "Fyodor Dostoevsky",
        "category": "Classic",
        "rating": 10,
        "cover_url": "/static/images/suc_ve_ceza.jpg",
        "summary": "Crime and Punishment follows Rodion Raskolnikov, a poor former student living in Saint Petersburg. He believes that some extraordinary people have the right to break moral rules if their actions serve a greater purpose. Driven by pride, poverty, and confused ideas about justice, he commits a terrible crime. However, after the act, he is not freed from suffering. Instead, he becomes trapped by guilt, fear, and emotional isolation. The novel explores the human conscience, the psychological weight of wrongdoing, and the possibility of redemption. Through Raskolnikov's inner conflict and his relationship with Sonya, Dostoevsky shows that punishment is not only legal but also deeply personal and spiritual."
    },
    "The Gambler": {
        "author": "Fyodor Dostoevsky",
        "category": "Classic",
        "rating": 8,
        "cover_url": "/static/images/kumarbaz.jpg",
        "summary": "The Gambler is a short novel about obsession, risk, love, and the destructive attraction of chance. The story follows Alexei Ivanovich, a young tutor working for a Russian family in a European resort town. Around him, people are controlled by debt, pride, romance, and the hope of sudden wealth. The roulette table becomes more than a game; it becomes a symbol of human weakness and emotional instability. Alexei believes he can control his luck, but the more he plays, the more he loses control of himself. Dostoevsky uses gambling to show how desire can become stronger than reason. The novel also reflects the author's own experience with gambling, making the emotions feel direct and realistic."
    },
    "Les Miserables": {
        "author": "Victor Hugo",
        "category": "Classic",
        "rating": 9,
        "cover_url": "/static/images/sefiller.jpg",
        "summary": "Les Miserables tells the powerful story of Jean Valjean, a man imprisoned for stealing bread and later judged harshly by society even after his release. After receiving kindness from a bishop, Valjean decides to change his life and become a better person. However, he is constantly pursued by Inspector Javert, who believes the law must be followed without mercy. The novel explores justice, poverty, forgiveness, sacrifice, and social inequality in nineteenth-century France. Through characters such as Fantine, Cosette, Marius, and Gavroche, Victor Hugo shows how personal lives are shaped by both love and suffering. At its heart, the book argues that compassion can transform people more deeply than punishment."
    },
    "Harry Potter": {
        "author": "J.K. Rowling",
        "category": "Fantasy",
        "rating": 9,
        "cover_url": "/static/images/harry_potter.jpg",
        "summary": "Harry Potter introduces the story of a young boy who discovers that he is a wizard and has a place at Hogwarts School of Witchcraft and Wizardry. Before this discovery, Harry lives an unhappy life with relatives who do not understand or care for him. At Hogwarts, he finds friendship, courage, and a sense of belonging. He also learns about his past and the dark wizard who changed his life forever. The story combines magic, mystery, school life, and adventure, but its strongest themes are friendship, loyalty, bravery, and the choice between good and evil. Harry's journey shows that family is not only about blood, but also about the people who stand beside us."
    },
    "The Hobbit": {
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
        "rating": 9,
        "cover_url": "/static/images/hobbit.jpg",
        "summary": "The Hobbit tells the story of Bilbo Baggins, a quiet and comfortable hobbit who is unexpectedly invited on an adventure by the wizard Gandalf and a group of dwarves. Their goal is to reclaim a lost treasure guarded by the dragon Smaug. At first, Bilbo seems too ordinary and fearful for such a dangerous journey, but as the adventure continues, he discovers courage, intelligence, and loyalty within himself. The story includes trolls, elves, riddles, mountains, and hidden dangers, but its main focus is Bilbo's personal growth. Tolkien presents adventure as a path that changes a person from the inside. By the end, Bilbo becomes someone brave enough to face the unknown."
    },
    "Dune": {
        "author": "Frank Herbert",
        "category": "Science Fiction",
        "rating": 8,
        "cover_url": "/static/images/dune.jpg",
        "summary": "Dune is set on the desert planet Arrakis, the only source of a valuable substance called spice. The story follows Paul Atreides, whose family is given control of Arrakis and quickly becomes trapped in a dangerous political conflict. As Paul learns about the planet, its people, and its harsh environment, he also begins to understand his own unusual abilities and destiny. The novel combines science fiction with politics, religion, ecology, and questions of leadership. Frank Herbert shows that power is never simple and that heroes can also become dangerous symbols. Dune is not only an adventure story, but also a warning about control, belief, and the cost of empire."
    },
    "Atomic Habits": {
        "author": "James Clear",
        "category": "Psychology",
        "rating": 9,
        "cover_url": "/static/images/atomic_habits.jpg",
        "summary": "Atomic Habits explains how small daily actions can create major long-term results. James Clear argues that success does not usually come from one dramatic change, but from tiny habits repeated consistently over time. The book presents practical ideas such as making good habits obvious, attractive, easy, and satisfying while making bad habits harder to continue. It also explains the importance of identity: instead of only focusing on goals, people should focus on becoming the kind of person who naturally performs the desired actions. The book is useful because it gives simple examples that can be applied to studying, health, work, and personal development. Its main message is that small improvements can compound into meaningful change."
    },
    "Thinking, Fast and Slow": {
        "author": "Daniel Kahneman",
        "category": "Psychology",
        "rating": 10,
        "cover_url": "/static/images/thinking_fast_and_slow.jpg",
        "summary": "Thinking, Fast and Slow explores how the human mind makes decisions. Daniel Kahneman describes two systems of thinking: one is fast, automatic, and emotional, while the other is slower, more careful, and logical. Many everyday decisions are influenced by mental shortcuts, and these shortcuts can sometimes lead to mistakes. The book explains ideas such as bias, confidence, loss aversion, and the way people judge risk. Although it is based on psychology and behavioral economics, the main lessons are useful in daily life. Kahneman shows that people are not always as rational as they believe. By understanding how thinking works, readers can become more aware of their own judgments and choices."
    },
    "Clean Code": {
        "author": "Robert C. Martin",
        "category": "Programming",
        "rating": 10,
        "cover_url": "/static/images/clean_code.jpg",
        "summary": "Clean Code is a programming book about writing code that is easy to read, understand, and maintain. Robert C. Martin explains that code is read many more times than it is written, so programmers should care about clarity and structure. The book discusses naming, functions, comments, formatting, error handling, and testing. Its main idea is that good code should communicate its purpose clearly and should not create unnecessary confusion for other developers. Although some examples are technical, the general message is simple: professional programmers should take responsibility for the quality of their work. Clean Code is useful for students because it teaches habits that make projects easier to improve and debug."
    },
    "Python Crash Course": {
        "author": "Eric Matthes",
        "category": "Programming",
        "rating": 9,
        "cover_url": "/static/images/python_crash_course.jpg",
        "summary": "Python Crash Course is a beginner-friendly programming book that teaches Python through clear explanations and practical projects. It starts with basic topics such as variables, lists, loops, functions, classes, and files. After building a foundation, it guides readers through projects that make the learning process more active and interesting. The book is helpful because it does not only explain syntax; it encourages students to build real things and learn by doing. For someone creating a website or learning software development, it provides a strong starting point. Its main value is that it makes programming feel possible, even for beginners, by breaking complex ideas into manageable steps."
    }
}

def get_book_data(title):
    return BOOK_DATA.get(title)


def calculate_average_rating(ratings):
    if len(ratings) == 0:
        return 0

    return sum(ratings) / len(ratings)


def is_top_rated(rating):
    return rating >= 9

def get_connection():
    return sqlite3.connect("library.db")


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            author TEXT,
            category TEXT,
            status TEXT,
            rating INTEGER,
            progress INTEGER,
            favorite INTEGER,
            cover_url TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


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