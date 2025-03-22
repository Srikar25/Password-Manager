import sqlite3
from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def load_or_generate_key():
    """Load or generate encryption key."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

key = load_or_generate_key()
cipher_suite = Fernet(key)

def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        app_name TEXT UNIQUE NOT NULL,
                        encrypted_password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def encrypt_password(password):
    """Encrypt password using AES (Fernet)."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """Decrypt password using AES (Fernet)."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def save_password(app_name, password):
    """Save encrypted password to database."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    encrypted_password = encrypt_password(password)
    cursor.execute("INSERT OR REPLACE INTO passwords (app_name, encrypted_password) VALUES (?, ?)",
                   (app_name, encrypted_password))
    conn.commit()
    conn.close()

def get_saved_apps(search_query=""):
    """Fetch saved application names."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT app_name FROM passwords WHERE app_name LIKE ?", ('%' + search_query + '%',))
    records = [row[0] for row in cursor.fetchall()]
    conn.close()
    return records

def get_decrypted_password(app_name):
    """Retrieve and decrypt password for given application."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password FROM passwords WHERE app_name = ?", (app_name,))
    record = cursor.fetchone()
    conn.close()
    return decrypt_password(record[0]) if record else None

def delete_password(app_name):
    """Delete password entry from database."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE app_name = ?", (app_name,))
    conn.commit()
    conn.close()

init_db()
