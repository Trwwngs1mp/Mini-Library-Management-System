import tkinter as tk
from tkinter import ttk, messagebox


class BookView:
    """View for managing books (CRUD + Search)."""

    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.selected_book_id = None
        self._build_ui()

    def _build_ui(self):
        # Search frame
        search_frame = ttk.LabelFrame(self.frame, text="Tìm kiếm sách", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Từ khóa:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self._search_books())

        # Form frame
        form_frame = ttk.LabelFrame(self.frame, text="Thông tin sách", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Tiêu đề:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Tác giả:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.author_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.author_var, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.isbn_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.isbn_var, width=30).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Năm XB:").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.year_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.year_var, width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Số lượng:").grid(row=1, column=2, padx=5, pady=2, sticky="e")
        self.qty_var = tk.StringVar(value="1")
        ttk.Entry(form_frame, textvariable=self.qty_var, width=15).grid(row=1, column=3, padx=5, pady=2)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(btn_frame, text="Thêm sách", command=self._add_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cập nhật", command=self._update_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa sách", command=self._delete_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa form", command=self._clear_form).pack(side="left", padx=5)

        # Table
        table_frame = ttk.LabelFrame(self.frame, text="Danh sách sách", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "title", "author", "isbn", "year", "quantity")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Tiêu đề")
        self.tree.heading("author", text="Tác giả")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("year", text="Năm XB")
        self.tree.heading("quantity", text="SL")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("isbn", width=120)
        self.tree.column("year", width=70, anchor="center")
        self.tree.column("quantity", width=50, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<ButtonRelease-1>", self._on_row_select)

    def refresh(self):
        """Refresh the book list."""
        self._load_books()

    def _load_books(self, keyword=""):
        """Load books into treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        books = self.controller.search_books(keyword)
        for b in books:
            self.tree.insert(
                "", "end",
                values=(b["id"], b["title"], b["author"],
                        b["isbn"], b["published_year"] or "", b["quantity"]),
            )

    def _search_books(self):
        keyword = self.search_var.get()
        self._load_books(keyword)

    def _add_book(self):
        result = self.controller.add_book(
            self.title_var.get(),
            self.author_var.get(),
            self.isbn_var.get(),
            self.year_var.get(),
            self.qty_var.get(),
        )
        if result["success"]:
            messagebox.showinfo("Thành công", "Đã thêm sách thành công!")
            self._clear_form()
            self._load_books()
        else:
            messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _update_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần cập nhật.")
            return
        result = self.controller.update_book(
            self.selected_book_id,
            self.title_var.get(),
            self.author_var.get(),
            self.isbn_var.get(),
            self.year_var.get(),
            self.qty_var.get(),
        )
        if result["success"]:
            messagebox.showinfo("Thành công", "Đã cập nhật sách thành công!")
            self._clear_form()
            self._load_books()
        else:
            messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _delete_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần xóa.")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sách này?"):
            result = self.controller.delete_book(self.selected_book_id)
            if result["success"]:
                messagebox.showinfo("Thành công", "Đã xóa sách!")
                self._clear_form()
                self._load_books()
            else:
                messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _clear_form(self):
        self.selected_book_id = None
        self.title_var.set("")
        self.author_var.set("")
        self.isbn_var.set("")
        self.year_var.set("")
        self.qty_var.set("1")

    def _on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        if not values:
            return
        self.selected_book_id = values[0]
        self.title_var.set(values[1])
        self.author_var.set(values[2])
        self.isbn_var.set(values[3])
        self.year_var.set(str(values[4]) if values[4] else "")
        self.qty_var.set(str(values[5]))