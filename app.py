from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(debug=True)