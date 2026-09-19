from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY completed, id DESC").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
        (title, priority, due_date)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET completed = 1 - completed WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    title = request.form["title"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    conn = get_db()
    conn.execute(
        "UPDATE tasks SET title = ?, priority = ?, due_date = ? WHERE id = ?",
        (title, priority, due_date, task_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
