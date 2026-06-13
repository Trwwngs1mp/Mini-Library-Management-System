from src.model.borrow_ticket import BorrowTicket
from src.model.book import Book
from src.model.reader import Reader
from src.model.database import Database


class BorrowController:
    """Controller for borrowing and returning operations."""

    def __init__(self, db: Database):
        self.borrow_model = BorrowTicket(db)
        self.book_model = Book(db)
        self.reader_model = Reader(db)

    def create_borrow(self, reader_id, book_id):
        """Create a borrow ticket."""
        reader = self.reader_model.get_reader_by_id(reader_id)
        if not reader:
            return {"success": False, "errors": ["Độc giả không tồn tại."]}

        book = self.book_model.get_book_by_id(book_id)
        if not book:
            return {"success": False, "errors": ["Sách không tồn tại."]}

        if book["quantity"] <= 0:
            return {"success": False, "errors": ["Sách đã hết, không thể mượn."]}

        ticket_id = self.borrow_model.create_ticket(reader_id, book_id)
        if ticket_id is None:
            return {"success": False, "errors": ["Sách đã hết, không thể mượn."]}

        return {"success": True, "ticket_id": ticket_id}

    def return_book(self, ticket_id):
        """Process returning a book."""
        result = self.borrow_model.return_book(ticket_id)
        if result is None:
            return {
                "success": False,
                "errors": ["Phiếu mượn không tồn tại hoặc đã được trả."],
            }
        return {"success": True, "fine": result["fine"]}

    def get_all_tickets(self):
        """Get all tickets."""
        return self.borrow_model.get_all_tickets()

    def get_active_tickets(self):
        """Get active (borrowed) tickets."""
        return self.borrow_model.get_active_tickets()

    def search_tickets(self, keyword):
        """Search tickets."""
        return self.borrow_model.search_tickets(keyword)

    def get_ticket_by_id(self, ticket_id):
        """Get a single ticket by ID."""
        return self.borrow_model.get_ticket_by_id(ticket_id)