import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class BorrowView:
    """View for managing borrowing and returning books."""

    def __init__(self, parent, borrow_controller, book_controller, reader_controller):
        self.borrow_controller = borrow_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self):
        # Borrow form
        borrow_frame = ttk.LabelFrame(self.frame, text="Tạo phiếu mượn", padding=10)
        borrow_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(borrow_frame, text="Độc giả (ID):").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.reader_id_var = tk.StringVar()
        ttk.Entry(borrow_frame, textvariable=self.reader_id_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(borrow_frame, text="...", command=self._select_reader, width=3).grid(row=0, column=2, padx=2)

        self.reader_info_var = tk.StringVar()
        ttk.Label(borrow_frame, textvariable=self.reader_info_var, foreground="gray").grid(row=0, column=3, padx=5, sticky="w")

        ttk.Label(borrow_frame, text="Sách (ID):").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.book_id_var = tk.StringVar()
        ttk.Entry(borrow_frame, textvariable=self.book_id_var, width=10).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(borrow_frame, text="...", command=self._select_book, width=3).grid(row=1, column=2, padx=2)

        self.book_info_var = tk.StringVar()
        ttk.Label(borrow_frame, textvariable=self.book_info_var, foreground="gray").grid(row=1, column=3, padx=5, sticky="w")

        ttk.Button(borrow_frame, text="Xác nhận mượn sách", command=self._borrow_book).grid(row=2, column=0, columnspan=4, pady=10)

        # Return form
        return_frame = ttk.LabelFrame(self.frame, text="Trả sách", padding=10)
        return_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(return_frame, text="Mã phiếu mượn:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.return_ticket_id_var = tk.StringVar()
        ttk.Entry(return_frame, textvariable=self.return_ticket_id_var, width=15).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(return_frame, text="Xác nhận trả sách", command=self._return_book).grid(row=0, column=2, padx=10)

        # Search
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Tìm kiếm:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self._search_tickets())

        # Tickets table
        table_frame = ttk.LabelFrame(self.frame, text="Danh sách phiếu mượn", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = (
            "id", "reader_name", "book_title", "borrow_date",
            "due_date", "return_date", "fine", "status"
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="Mã PM")
        self.tree.heading("reader_name", text="Độc giả")
        self.tree.heading("book_title", text="Sách")
        self.tree.heading("borrow_date", text="Ngày mượn")
        self.tree.heading("due_date", text="Hạn trả")
        self.tree.heading("return_date", text="Ngày trả")
        self.tree.heading("fine", text="Phạt (VNĐ)")
        self.tree.heading("status", text="Trạng thái")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("reader_name", width=150)
        self.tree.column("book_title", width=180)
        self.tree.column("borrow_date", width=100)
        self.tree.column("due_date", width=100)
        self.tree.column("return_date", width=100)
        self.tree.column("fine", width=100, anchor="e")
        self.tree.column("status", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-Button-1>", self._on_ticket_double_click)

    def refresh(self):
        self._load_tickets()

    def _load_tickets(self, keyword=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tickets = self.borrow_controller.search_tickets(keyword)
        for t in tickets:
            status_text = "Đã mượn" if t["status"] == "borrowed" else "Đã trả"
            self.tree.insert(
                "", "end",
                values=(
                    t["id"],
                    t["reader_name"],
                    t["book_title"],
                    t["borrow_date"],
                    t["due_date"],
                    t["return_date"] or "",
                    f"{t['fine']:,.0f}" if t.get("fine") else "0",
                    status_text,
                ),
            )

    def _search_tickets(self):
        keyword = self.search_var.get()
        self._load_tickets(keyword)

    def _select_reader(self):
        dialog = SelectDialog(
            self.frame,
            "Chọn độc giả",
            self.reader_controller.get_all_readers(),
            ["id", "name", "email", "phone"],
            "id",
        )
        if dialog.result:
            self.reader_id_var.set(str(dialog.result["id"]))
            self.reader_info_var.set(f"{dialog.result['name']} - {dialog.result['email']}")

    def _select_book(self):
        dialog = SelectDialog(
            self.frame,
            "Chọn sách",
            self.book_controller.get_all_books(),
            ["id", "title", "author", "isbn", "quantity"],
            "id",
        )
        if dialog.result:
            self.book_id_var.set(str(dialog.result["id"]))
            self.book_info_var.set(
                f"{dialog.result['title']} - {dialog.result['author']} (SL: {dialog.result['quantity']})"
            )

    def _borrow_book(self):
        reader_id = self.reader_id_var.get()
        book_id = self.book_id_var.get()

        if not reader_id or not book_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn độc giả và sách.")
            return

        try:
            reader_id = int(reader_id)
            book_id = int(book_id)
        except ValueError:
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return

        result = self.borrow_controller.create_borrow(reader_id, book_id)
        if result["success"]:
            messagebox.showinfo("Thành công", f"Đã tạo phiếu mượn! Mã phiếu: {result['ticket_id']}")
            self.reader_id_var.set("")
            self.book_id_var.set("")
            self.reader_info_var.set("")
            self.book_info_var.set("")
            self._load_tickets()
        else:
            messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _return_book(self):
        ticket_id = self.return_ticket_id_var.get()
        if not ticket_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu mượn.")
            return

        try:
            ticket_id = int(ticket_id)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã phiếu không hợp lệ.")
            return

        # Check ticket info first
        ticket = self.borrow_controller.get_ticket_by_id(ticket_id)
        if not ticket:
            messagebox.showerror("Lỗi", "Phiếu mượn không tồn tại.")
            return
        if ticket["status"] == "returned":
            messagebox.showwarning("Cảnh báo", "Phiếu này đã được trả trước đó.")
            return

        result = self.borrow_controller.return_book(ticket_id)
        if result["success"]:
            msg = "Trả sách thành công!"
            if result["fine"] > 0:
                msg += f"\nTiền phạt trễ hạn: {result['fine']:,.0f} VNĐ"
            messagebox.showinfo("Thành công", msg)
            self.return_ticket_id_var.set("")
            self._load_tickets()
        else:
            messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _on_ticket_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        if not values:
            return
        # Auto-fill return ticket ID
        self.return_ticket_id_var.set(str(values[0]))


class SelectDialog:
    """A simple dialog to select an item from a list."""

    def __init__(self, parent, title, items, columns, id_column):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.items = items
        self.id_column = id_column

        # Search
        search_frame = ttk.Frame(self.dialog)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Tìm:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self._filter())

        # Treeview
        tree_frame = ttk.Frame(self.dialog)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-Button-1>", self._select)

        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Chọn", command=self._select).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.dialog.destroy).pack(side="right", padx=5)

        self._load_data(items)

        self.dialog.wait_window()

    def _load_data(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for d in data:
            values = [str(d.get(col, "")) for col in self.tree["columns"]]
            self.tree.insert("", "end", values=values)

    def _filter(self):
        keyword = self.search_var.get().lower()
        if not keyword:
            self._load_data(self.items)
            return
        filtered = [
            item for item in self.items
            if any(keyword in str(v).lower() for v in item.values())
        ]
        self._load_data(filtered)

    def _select(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        cols = self.tree["columns"]
        result_dict = {}
        for i, col in enumerate(cols):
            if i < len(values):
                result_dict[col] = values[i]
        self.result = result_dict
        self.dialog.destroy()