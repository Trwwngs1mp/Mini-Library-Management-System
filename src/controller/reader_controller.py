from src.model.reader import Reader
from src.model.database import Database


class ReaderController:
    """Controller for reader-related operations."""

    def __init__(self, db: Database):
        self.reader_model = Reader(db)

    def add_reader(self, name, email, phone):
        """Validate and add a reader."""
        errors = []
        if not name.strip():
            errors.append("Tên độc giả không được để trống.")
        if not email.strip():
            errors.append("Email không được để trống.")
        if "@" not in email or "." not in email:
            errors.append("Email không hợp lệ.")

        if errors:
            return {"success": False, "errors": errors}

        try:
            reader_id = self.reader_model.add_reader(
                name.strip(), email.strip(), phone.strip()
            )
            return {"success": True, "reader_id": reader_id}
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return {"success": False, "errors": ["Email đã tồn tại trong hệ thống."]}
            return {"success": False, "errors": [str(e)]}

    def update_reader(self, reader_id, name, email, phone):
        """Validate and update a reader."""
        errors = []
        if not name.strip():
            errors.append("Tên độc giả không được để trống.")
        if not email.strip():
            errors.append("Email không được để trống.")

        if errors:
            return {"success": False, "errors": errors}

        try:
            self.reader_model.update_reader(
                reader_id, name.strip(), email.strip(), phone.strip()
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "errors": [str(e)]}

    def delete_reader(self, reader_id):
        """Delete a reader."""
        try:
            self.reader_model.delete_reader(reader_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "errors": [str(e)]}

    def get_all_readers(self):
        """Get all readers."""
        return self.reader_model.get_all_readers()

    def get_reader_by_id(self, reader_id):
        """Get a reader by ID."""
        return self.reader_model.get_reader_by_id(reader_id)

    def search_readers(self, keyword):
        """Search readers."""
        return self.reader_model.search_readers(keyword)

    def get_borrow_history(self, reader_id):
        """Get borrow history for a reader."""
        return self.reader_model.get_borrow_history(reader_id)