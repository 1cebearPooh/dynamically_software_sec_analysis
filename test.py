from flask import Flask, request, jsonify
import sqlite3
import os
import signal

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, age INTEGER)''')
    c.execute("INSERT INTO users (username, age) VALUES ('Alice', 30)")
    c.execute("INSERT INTO users (username, age) VALUES ('Bob', 25)")
    conn.commit()


@app.route('/')
def index():
    return "Welcome to the insecure app!"


@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username', '')
    query = f"SELECT * FROM users WHERE username = '{username}'"
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return jsonify(result)


def signal_handler(signum, frame):
    print("Signal received:", signum)
    os._exit(0)


if __name__ == '__main__':
    init_db()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    app.run(debug=True)
