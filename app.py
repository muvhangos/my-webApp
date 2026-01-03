from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "users.db"


def get_db():
    return sqlite3.connect(DATABASE)


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cursor = db.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            role TEXT
        )
    """)

    # Add user
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        role = request.form["role"]

        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (name, email, role)
        )
        db.commit()
        return redirect(url_for("index"))

    # Fetch users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    db.close()

    return render_template("index.html", users=users)


@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
