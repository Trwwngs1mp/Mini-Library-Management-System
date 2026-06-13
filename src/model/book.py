from src.model.database import Database


class Book:
    """Book model - handles all book-related database operations."""

    def __init__(self, db: Database):
        self.db = db

    def add_book(self, title, author, isbn, published_year=None, quantity=1, image_url=None):
        """Add a new book. Returns the new book ID or None if ISBN exists."""
        try:
            cursor = self.db.execute(
                """INSERT INTO books (title, author, isbn, published_year, quantity, image_url)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (title, author, isbn, published_year, quantity, image_url),
            )
            return cursor.lastrowid
        except Exception as e:
            raise e

    def update_book(self, book_id, title, author, isbn, published_year, quantity, image_url=None):
        """Update an existing book."""
        self.db.execute(
            """UPDATE books SET title=?, author=?, isbn=?, published_year=?, quantity=?, image_url=?
               WHERE id=?""",
            (title, author, isbn, published_year, quantity, image_url, book_id),
        )

    def delete_book(self, book_id):
        """Delete a book by ID."""
        self.db.execute("DELETE FROM books WHERE id=?", (book_id,))

    def get_book_by_id(self, book_id):
        """Get a single book by ID."""
        row = self.db.fetch_one("SELECT * FROM books WHERE id=?", (book_id,))
        return dict(row) if row else None

    def search_books(self, keyword=""):
        """Search books by title, author, or ISBN."""
        if keyword:
            like_pattern = f"%{keyword}%"
            rows = self.db.fetch_all(
                """SELECT * FROM books
                   WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
                   ORDER BY title""",
                (like_pattern, like_pattern, like_pattern),
            )
        else:
            rows = self.db.fetch_all("SELECT * FROM books ORDER BY title")
        return [dict(row) for row in rows]

    def get_all_books(self):
        """Get all books."""
        return self.search_books()

    def borrow_book(self, book_id):
        """Decrease quantity by 1 when borrowing. Returns True if successful."""
        book = self.get_book_by_id(book_id)
        if book and book["quantity"] > 0:
            self.db.execute(
                "UPDATE books SET quantity = quantity - 1 WHERE id=?",
                (book_id,),
            )
            return True
        return False

    def return_book(self, book_id):
        """Increase quantity by 1 when returning."""
        self.db.execute(
            "UPDATE books SET quantity = quantity + 1 WHERE id=?",
            (book_id,),
        )