from src.model.database import Database


class Reader:
    """Reader model - handles all reader-related database operations."""

    def __init__(self, db: Database):
        self.db = db

    def add_reader(self, name, email, phone=""):
        """Add a new reader. Returns the new reader ID or raises error."""
        try:
            cursor = self.db.execute(
                "INSERT INTO readers (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone),
            )
            return cursor.lastrowid
        except Exception as e:
            raise e

    def update_reader(self, reader_id, name, email, phone):
        """Update an existing reader."""
        self.db.execute(
            "UPDATE readers SET name=?, email=?, phone=? WHERE id=?",
            (name, email, phone, reader_id),
        )

    def delete_reader(self, reader_id):
        """Delete a reader by ID."""
        self.db.execute("DELETE FROM readers WHERE id=?", (reader_id,))

    def get_reader_by_id(self, reader_id):
        """Get a single reader by ID."""
        row = self.db.fetch_one("SELECT * FROM readers WHERE id=?", (reader_id,))
        return dict(row) if row else None

    def search_readers(self, keyword=""):
        """Search readers by name, email, or phone."""
        if keyword:
            like_pattern = f"%{keyword}%"
            rows = self.db.fetch_all(
                """SELECT * FROM readers
                   WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
                   ORDER BY name""",
                (like_pattern, like_pattern, like_pattern),
            )
        else:
            rows = self.db.fetch_all("SELECT * FROM readers ORDER BY name")
        return [dict(row) for row in rows]

    def get_all_readers(self):
        """Get all readers."""
        return self.search_readers()

    def get_borrow_history(self, reader_id):
        """Get borrowing history for a reader."""
        rows = self.db.fetch_all(
            """SELECT bt.*, b.title AS book_title, b.author AS book_author
               FROM borrow_tickets bt
               JOIN books b ON bt.book_id = b.id
               WHERE bt.reader_id = ?
               ORDER BY bt.borrow_date DESC""",
            (reader_id,),
        )
        return [dict(row) for row in rows]