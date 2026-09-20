import sqlite3
import pickle
import os
from flask import Flask, request

app = Flask(__name__)

# УЯЗВИМОСТЬ 1: Жёстко закодированные секреты
SECRET_KEY = "hardcoded-secret-abc123"
DB_PASSWORD = "admin123"

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # УЯЗВИМОСТЬ 2: SQL-инъекция (f-string в SQL-запросе)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(query)
    return str(cursor.fetchall())

@app.route("/deserialize", methods=["POST"])
def deserialize():
    # УЯЗВИМОСТЬ 3: Небезопасная десериализация pickle
    data = request.get_data()
    obj = pickle.loads(data)
    return str(obj)

@app.route("/ping", methods=["GET"])
def ping():
    # УЯЗВИМОСТЬ 4: Command Injection
    host = request.args.get("host", "127.0.0.1")
    result = os.popen(f"ping -c 1 {host}").read()
    return result

if __name__ == "__main__":
    # УЯЗВИМОСТЬ 5: debug=True в production
    app.run(debug=True)
