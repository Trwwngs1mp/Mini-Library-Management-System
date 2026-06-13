import sqlite3
import os


class Database:
    """SQLite Database helper for Mini Library Management System."""

    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "library.db")

    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = Database.DB_PATH
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """Create connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def _create_tables(self):
        """Create the required tables if they don't exist."""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                published_year INTEGER,
                quantity INTEGER NOT NULL DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reader_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL DEFAULT (date('now')),
                due_date TEXT NOT NULL,
                return_date TEXT,
                fine REAL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'borrowed',
                FOREIGN KEY (reader_id) REFERENCES readers(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """)

        self.conn.commit()

    def execute(self, query, params=None):
        """Execute a query and return cursor."""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor

    def fetch_all(self, query, params=None):
        """Fetch all rows."""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        """Fetch one row."""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()