from src.model.book import Book
from src.model.database import Database


class BookController:
    """Controller for book-related operations."""

    def __init__(self, db: Database):
        self.book_model = Book(db)

    def add_book(self, title, author, isbn, published_year, quantity):
        """Validate and add a book."""
        errors = []
        if not title.strip():
            errors.append("Tiêu đề sách không được để trống.")
        if not author.strip():
            errors.append("Tác giả không được để trống.")
        if not isbn.strip():
            errors.append("ISBN không được để trống.")
        try:
            qty = int(quantity)
            if qty < 1:
                errors.append("Số lượng phải >= 1.")
        except ValueError:
            errors.append("Số lượng phải là số nguyên.")

        if errors:
            return {"success": False, "errors": errors}

        try:
            book_id = self.book_model.add_book(
                title.strip(),
                author.strip(),
                isbn.strip(),
                published_year if published_year.strip() else None,
                qty,
            )
            return {"success": True, "book_id": book_id}
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return {"success": False, "errors": ["ISBN đã tồn tại trong hệ thống."]}
            return {"success": False, "errors": [str(e)]}

    def update_book(self, book_id, title, author, isbn, published_year, quantity):
        """Validate and update a book."""
        errors = []
        if not title.strip():
            errors.append("Tiêu đề sách không được để trống.")
        if not author.strip():
            errors.append("Tác giả không được để trống.")
        if not isbn.strip():
            errors.append("ISBN không được để trống.")
        try:
            qty = int(quantity)
            if qty < 0:
                errors.append("Số lượng không được âm.")
        except ValueError:
            errors.append("Số lượng phải là số nguyên.")

        if errors:
            return {"success": False, "errors": errors}

        try:
            self.book_model.update_book(
                book_id,
                title.strip(),
                author.strip(),
                isbn.strip(),
                published_year if published_year.strip() else None,
                qty,
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "errors": [str(e)]}

    def delete_book(self, book_id):
        """Delete a book."""
        try:
            self.book_model.delete_book(book_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "errors": [str(e)]}

    def get_all_books(self):
        """Get all books."""
        return self.book_model.get_all_books()

    def get_book_by_id(self, book_id):
        """Get a book by ID."""
        return self.book_model.get_book_by_id(book_id)

    def search_books(self, keyword):
        """Search books."""
        return self.book_model.search_books(keyword)