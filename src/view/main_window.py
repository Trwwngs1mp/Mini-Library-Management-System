import tkinter as tk
from tkinter import ttk, messagebox
from src.controller.book_controller import BookController
from src.controller.reader_controller import ReaderController
from src.controller.borrow_controller import BorrowController
from src.model.database import Database
from src.view.book_view import BookView
from src.view.reader_view import ReaderView
from src.view.borrow_view import BorrowView


class MainWindow:
    """Main application window with tabbed interface."""

    def __init__(self, root):
        self.root = root
        self.root.title("Mini Library Management System")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)

        # Center window on screen
        self._center_window()

        # Initialize database and controllers
        self.db = Database()
        self.book_controller = BookController(self.db)
        self.reader_controller = ReaderController(self.db)
        self.borrow_controller = BorrowController(self.db)

        # Build UI
        self._build_menu()
        self._build_tabs()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Thoát", command=self._on_close, accelerator="Ctrl+Q")
        self.root.bind("<Control-q>", lambda e: self._on_close())

    def _build_tabs(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Tab 1: Manage Books
        self.book_view = BookView(self.notebook, self.book_controller)
        self.notebook.add(self.book_view.frame, text="📚 Quản lý sách")

        # Tab 2: Manage Readers
        self.reader_view = ReaderView(self.notebook, self.reader_controller)
        self.notebook.add(self.reader_view.frame, text="👤 Quản lý độc giả")

        # Tab 3: Borrow/Return
        self.borrow_view = BorrowView(
            self.notebook,
            self.borrow_controller,
            self.book_controller,
            self.reader_controller,
        )
        self.notebook.add(self.borrow_view.frame, text="📋 Mượn/Trả sách")

        # Refresh data when tab changes
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event=None):
        """Refresh data when switching tabs."""
        selected = self.notebook.index(self.notebook.select())
        if selected == 0:
            self.book_view.refresh()
        elif selected == 1:
            self.reader_view.refresh()
        elif selected == 2:
            self.borrow_view.refresh()

    def _on_close(self):
        """Clean up and close the application."""
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát?"):
            self.db.close()
            self.root.destroy()