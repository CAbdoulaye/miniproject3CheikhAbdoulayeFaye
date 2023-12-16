import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_FILE = 'users.db'

def create_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_title TEXT NOT NULL,
            review_text TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')

    conn.commit()
    conn.close()

def register_user(username, email, password, confirm_password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False  # User already exists

    # Additional check for password matching confirm_password
    if password != confirm_password:
        conn.close()
        return False  # Passwords do not match

    # Use a valid hash method for generate_password_hash
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash))
    conn.commit()
    conn.close()
    return True  # Registration successful


def login_user(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[3], password):  # Assuming password_hash is in the fourth column
        return user  # Return the user object on successful login
    else:
        return None  # Login failed


def add_review(user_id, movie_title, review_text):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO reviews (user_id, movie_title, review_text) VALUES (?, ?, ?)', (user_id, movie_title, review_text))
    conn.commit()
    conn.close()


def get_reviews_by_movie(movie_title):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT review_text FROM reviews WHERE movie_title=?', (movie_title,))
    reviews = cursor.fetchall()

    conn.close()
    return reviews