# Mini Library Management System

Hệ thống quản lý thư viện mini - Bài tập thực hành quản lý mã nguồn và lập trình giao diện.

## Công nghệ sử dụng

- **Ngôn ngữ:** Python 3
- **GUI:** Tkinter (thư viện chuẩn của Python)
- **Cơ sở dữ liệu:** SQLite
- **Kiến trúc:** MVC (Model-View-Controller)

## Chức năng

### 1. Quản lý sách (📚)
- Thêm sách mới (tiêu đề, tác giả, ISBN, năm xuất bản, số lượng)
- Sửa thông tin sách
- Xóa sách
- Tìm kiếm sách theo từ khóa (tiêu đề, tác giả, ISBN)

### 2. Quản lý độc giả (👤)
- Đăng ký độc giả mới (họ tên, email, số điện thoại)
- Sửa thông tin độc giả
- Xóa độc giả
- Tìm kiếm độc giả
- Xem lịch sử mượn sách của độc giả

### 3. Mượn/Trả sách (📋)
- Tạo phiếu mượn (chọn độc giả + sách, tự động tính hạn trả 14 ngày)
- Kiểm tra số lượng sách: thông báo "Đã hết sách" nếu số lượng = 0
- Trả sách: tự động tính tiền phạt (2,000 VNĐ/ngày trễ hạn)
- Xem danh sách tất cả phiếu mượn
- Tìm kiếm phiếu mượn

## Cài đặt

### Yêu cầu
- Python 3.6 trở lên (Python 3.13 đã được kiểm tra)

### Các bước cài đặt

1. **Clone repository**
   ```bash
   git clone https://github.com/Trwwngs1mp/Mini-Library-Management-System.git
   cd Mini-Library-Management-System
   ```

2. **Chạy ứng dụng** (không cần cài đặt thêm thư viện)
   ```bash
   python main.py
   ```

   Hoặc:
   ```bash
   python3 main.py
   ```

## Cấu trúc thư mục

```
Mini-Library-Management-System/
├── main.py                      # Entry point
├── src/
│   ├── __init__.py
│   ├── model/                   # Model - Dữ liệu
│   │   ├── __init__.py
│   │   ├── database.py          # Kết nối SQLite
│   │   ├── book.py              # Book model
│   │   ├── reader.py            # Reader model
│   │   └── borrow_ticket.py     # BorrowTicket model
│   ├── controller/              # Controller - Logic xử lý
│   │   ├── __init__.py
│   │   ├── book_controller.py
│   │   ├── reader_controller.py
│   │   └── borrow_controller.py
│   └── view/                    # View - Giao diện
│       ├── __init__.py
│       ├── main_window.py
│       ├── book_view.py
│       ├── reader_view.py
│       └── borrow_view.py
├── .gitignore
└── README.md
```

## Git Branching Strategy

Dự án sử dụng **Git Feature Branch Workflow**:

1. **Nhánh `main`**: Nhánh chính, code ổn định
2. **Nhánh feature**: Phát triển từng tính năng riêng biệt
   - `feature/manage-books` - Quản lý sách
   - `feature/manage-readers` - Quản lý độc giả
   - `feature/borrow-ticket` - Mượn/Trả sách

Quy trình:
```
main ────┬──── feature/manage-books ──► Merge PR #1
         ├──── feature/manage-readers ──► Merge PR #2
         └──── feature/borrow-ticket ──► Merge PR #3
```

## Tác giả

Bài tập môn: Lập trình giao diện và quản lý mã nguồn