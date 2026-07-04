
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path="./storage/database.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        print("Database connected successfully!")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Database disconnected!")

    def execute(self, query, params=None):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except Exception as e:
            print(f"Database error: {e}")
            self.connection.rollback()
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute(query, params)
        if cursor:
            return cursor.fetchall()
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute(query, params)
        if cursor:
            return cursor.fetchone()
        return None

    def initialize_tables(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Database tables initialized!")


db = Database()
