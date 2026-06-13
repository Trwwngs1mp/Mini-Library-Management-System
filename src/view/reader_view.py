import tkinter as tk
from tkinter import ttk, messagebox


class ReaderView:
    """View for managing readers (CRUD + Search + History)."""

    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.selected_reader_id = None
        self._build_ui()

    def _build_ui(self):
        # Search frame
        search_frame = ttk.LabelFrame(self.frame, text="Tìm kiếm độc giả", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Từ khóa:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self._search_readers())

        # Form frame
        form_frame = ttk.LabelFrame(self.frame, text="Thông tin độc giả", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="SĐT:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var, width=30).grid(row=2, column=1, padx=5, pady=2)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Thêm độc giả", command=self._add_reader).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cập nhật", command=self._update_reader).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa độc giả", command=self._delete_reader).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa form", command=self._clear_form).pack(side="left", padx=5)

        # Reader table
        table_frame = ttk.LabelFrame(self.frame, text="Danh sách độc giả", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "name", "email", "phone", "created_at")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Họ tên")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="SĐT")
        self.tree.heading("created_at", text="Ngày tạo")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=160)
        self.tree.column("email", width=180)
        self.tree.column("phone", width=120)
        self.tree.column("created_at", width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<ButtonRelease-1>", self._on_row_select)
        self.tree.bind("<Double-Button-1>", self._show_history)

        # History section
        history_frame = ttk.LabelFrame(self.frame, text="Lịch sử mượn sách", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns2 = ("id", "book_title", "borrow_date", "due_date", "return_date", "fine", "status")
        self.history_tree = ttk.Treeview(history_frame, columns=columns2, show="headings", height=5)
        self.history_tree.heading("id", text="ID")
        self.history_tree.heading("book_title", text="Sách")
        self.history_tree.heading("borrow_date", text="Ngày mượn")
        self.history_tree.heading("due_date", text="Hạn trả")
        self.history_tree.heading("return_date", text="Ngày trả")
        self.history_tree.heading("fine", text="Phạt (VNĐ)")
        self.history_tree.heading("status", text="Trạng thái")

        self.history_tree.column("id", width=40, anchor="center")
        self.history_tree.column("book_title", width=180)
        self.history_tree.column("borrow_date", width=100)
        self.history_tree.column("due_date", width=100)
        self.history_tree.column("return_date", width=100)
        self.history_tree.column("fine", width=100, anchor="e")
        self.history_tree.column("status", width=80, anchor="center")

        scrollbar2 = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar2.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")

    def refresh(self):
        self._load_readers()

    def _load_readers(self, keyword=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        readers = self.controller.search_readers(keyword)
        for r in readers:
            self.tree.insert(
                "", "end",
                values=(r["id"], r["name"], r["email"],
                        r["phone"] or "", r["created_at"] or ""),
            )

    def _search_readers(self):
        keyword = self.search_var.get()
        self._load_readers(keyword)

    def _add_reader(self):
        result = self.controller.add_reader(
            self.name_var.get(),
            self.email_var.get(),
            self.phone_var.get(),
        )
        if result["success"]:
            messagebox.showinfo("Thành công", "Đã thêm độc giả thành công!")
            self._clear_form()
            self._load_readers()
        else:
            messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _update_reader(self):
        if not self.selected_reader_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn độc giả cần cập nhật.")
            return
        result = self.controller.update_reader(
            self.selected_reader_id,
            self.name_var.get(),
            self.email_var.get(),
            self.phone_var.get(),
        )
        if result["success"]:
            messagebox.showinfo("Thành công", "Đã cập nhật độc giả!")
            self._clear_form()
            self._load_readers()
        else:
            messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _delete_reader(self):
        if not self.selected_reader_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn độc giả cần xóa.")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa độc giả này?"):
            result = self.controller.delete_reader(self.selected_reader_id)
            if result["success"]:
                messagebox.showinfo("Thành công", "Đã xóa độc giả!")
                self._clear_form()
                self._load_readers()
            else:
                messagebox.showerror("Lỗi", "\n".join(result["errors"]))

    def _clear_form(self):
        self.selected_reader_id = None
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        # Clear history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

    def _on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        if not values:
            return
        self.selected_reader_id = values[0]
        self.name_var.set(values[1])
        self.email_var.set(values[2])
        self.phone_var.set(str(values[3]) if values[3] else "")

    def _show_history(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        if not values:
            return
        reader_id = values[0]
        self._load_history(reader_id)

    def _load_history(self, reader_id):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        history = self.controller.get_borrow_history(reader_id)
        for h in history:
            status_text = "Đã mượn" if h["status"] == "borrowed" else "Đã trả"
            self.history_tree.insert(
                "", "end",
                values=(
                    h["id"],
                    h["book_title"],
                    h["borrow_date"],
                    h["due_date"],
                    h["return_date"] or "",
                    f"{h['fine']:,.0f}" if h["fine"] else "0",
                    status_text,
                ),
            )