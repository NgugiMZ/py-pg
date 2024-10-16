from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",  # Replace with your PostgreSQL database
        user="postgres",      # Replace with your database user
        password="optimus"    # Replace with your database password
    )
    return conn

# Utility function to validate email
def is_valid_email(email: str) -> bool:
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(email_regex, email))  # Convert match object to bool

# Utility function to validate password strength
def is_valid_password(password: str) -> bool:
    # Password must contain at least 8 characters, including numbers and special characters
    has_length = len(password) >= 8
    has_number = re.search(r"\d", password) is not None
    has_special = re.search(r"\W", password) is not None
    return has_length and has_number and has_special


@app.route('/')
def index():
    return render_template('index.html')  # Render the registration form

@app.route('/user-list')
def user_list():
    # Simulate a list of users for now
    users = [
        {'id': 1, 'username': 'john_doe', 'email': 'john@example.com'},
        {'id': 2, 'username': 'jane_doe', 'email': 'jane@example.com'}
    ]
    return render_template('user-list.html', users=users)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Basic input validation
    if not username or not password or not email:
        return jsonify({"error": "Username, password, and email are required"}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Validate password strength
    if not is_valid_password(password):
        return jsonify({
            "error": "Password must be at least 8 characters long, contain at least one number, and one special character."
        }), 400

    # Hash the password for security using Werkzeug's security functions
    hashed_password = generate_password_hash(password)

    # Save user to the database
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check if the username or email already exists
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 409

        # Insert new user
        cur.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, hashed_password, email)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Fetch user from the database
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
