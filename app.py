from flask import Flask, request, jsonify, render_template, Response
import pyodbc
import time
from prometheus_client import Histogram, generate_latest, Counter
from queue import Queue

app = Flask(__name__)

# Prometheus metrics
LOGIN_DURATION = Histogram('login_duration_seconds', 'Time spent processing login')
LOGIN_ATTEMPTS = Counter('login_attempts_total', 'Total login attempts')
LOGIN_SUCCESS = Counter('login_success_total', 'Total successful logins')
LOGIN_FAILED = Counter('login_failed_total', 'Total failed logins')

# Connection Pool
def create_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'
        'DATABASE=LoginSystem;'
        'Trusted_Connection=yes;'
    )

# Create a pool of 20 connections
connection_pool = Queue(maxsize=20)
for _ in range(20):
    connection_pool.put(create_connection())

def get_db():
    return connection_pool.get()

def return_db(conn):
    connection_pool.put(conn)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    LOGIN_ATTEMPTS.inc()
    start = time.time()

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
    finally:
        return_db(conn)

    duration = time.time() - start
    LOGIN_DURATION.observe(duration)

    if user:
        LOGIN_SUCCESS.inc()
        return jsonify({"status": "success", "response_time": round(duration, 4)})
    else:
        LOGIN_FAILED.inc()
        return jsonify({"status": "failed", "response_time": round(duration, 4)})

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
