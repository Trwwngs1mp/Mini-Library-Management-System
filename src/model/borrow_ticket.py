from datetime import datetime, timedelta
from src.model.database import Database


class BorrowTicket:
    """BorrowTicket model - handles borrowing and returning operations."""

    def __init__(self, db: Database):
        self.db = db

    def create_ticket(self, reader_id, book_id, due_days=14):
        """Create a new borrow ticket. Returns ticket ID or None if no stock."""
        from src.model.book import Book

        book_model = Book(self.db)
        if not book_model.borrow_book(book_id):
            return None  # Out of stock

        due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")
        cursor = self.db.execute(
            """INSERT INTO borrow_tickets (reader_id, book_id, due_date)
               VALUES (?, ?, ?)""",
            (reader_id, book_id, due_date),
        )
        return cursor.lastrowid

    def return_book(self, ticket_id):
        """Process returning a book. Calculates fine if overdue."""
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket or ticket["status"] == "returned":
            return None

        return_date = datetime.now().strftime("%Y-%m-%d")
        due_date = datetime.strptime(ticket["due_date"], "%Y-%m-%d")
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")

        fine = 0
        if return_dt > due_date:
            days_overdue = (return_dt - due_date).days
            fine = days_overdue * 2000  # 2000 VND per day overdue

        self.db.execute(
            """UPDATE borrow_tickets
               SET return_date=?, fine=?, status='returned'
               WHERE id=?""",
            (return_date, fine, ticket_id),
        )

        # Update book quantity
        from src.model.book import Book

        book_model = Book(self.db)
        book_model.return_book(ticket["book_id"])

        return {"fine": fine, "return_date": return_date}

    def get_ticket_by_id(self, ticket_id):
        """Get a single ticket by ID."""
        row = self.db.fetch_one("SELECT * FROM borrow_tickets WHERE id=?", (ticket_id,))
        return dict(row) if row else None

    def get_all_tickets(self):
        """Get all borrow tickets with book and reader info."""
        rows = self.db.fetch_all(
            """SELECT bt.*, b.title AS book_title, b.author AS book_author,
                      r.name AS reader_name, r.email AS reader_email
               FROM borrow_tickets bt
               JOIN books b ON bt.book_id = b.id
               JOIN readers r ON bt.reader_id = r.id
               ORDER BY bt.borrow_date DESC"""
        )
        return [dict(row) for row in rows]

    def get_active_tickets(self):
        """Get currently borrowed (not returned) tickets."""
        rows = self.db.fetch_all(
            """SELECT bt.*, b.title AS book_title, b.author AS book_author,
                      r.name AS reader_name, r.email AS reader_email
               FROM borrow_tickets bt
               JOIN books b ON bt.book_id = b.id
               JOIN readers r ON bt.reader_id = r.id
               WHERE bt.status = 'borrowed'
               ORDER BY bt.borrow_date DESC"""
        )
        return [dict(row) for row in rows]

    def search_tickets(self, keyword=""):
        """Search tickets by reader name, book title, etc."""
        if not keyword:
            return self.get_all_tickets()

        like_pattern = f"%{keyword}%"
        rows = self.db.fetch_all(
            """SELECT bt.*, b.title AS book_title, b.author AS book_author,
                      r.name AS reader_name, r.email AS reader_email
               FROM borrow_tickets bt
               JOIN books b ON bt.book_id = b.id
               JOIN readers r ON bt.reader_id = r.id
               WHERE r.name LIKE ? OR b.title LIKE ? OR r.email LIKE ?
               ORDER BY bt.borrow_date DESC""",
            (like_pattern, like_pattern, like_pattern),
        )
        return [dict(row) for row in rows]