# Mini Library Management System

Hệ thống quản lý thư viện mini - Bài tập thực hành quản lý mã nguồn và lập trình giao diện.

## Công nghệ sử dụng

- **Ngôn ngữ:** Python 3, JavaScript (ES6+)
- **Backend:** Flask (Python web framework)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Giao diện:** Dark Theme hiện đại
- **Cơ sở dữ liệu:** SQLite
- **Kiến trúc:** MVC (Model-View-Controller) + REST API

## Chức năng

### Dashboard (📊)
- Thống kê tổng quan: số sách, độc giả, phiếu đang mượn, tổng tiền phạt
- Truy cập nhanh đến các chức năng

### 1. Quản lý sách (📚)
- Thêm sách mới (tiêu đề, tác giả, ISBN, năm xuất bản, số lượng, **ảnh bìa**)
- Sửa thông tin sách
- Xóa sách
- Tìm kiếm sách theo từ khóa (tiêu đề, tác giả, ISBN)
- Hiển thị dạng lưới với ảnh bìa

### 2. Quản lý độc giả (👤)
- Đăng ký độc giả mới (họ tên, email, số điện thoại)
- Sửa thông tin độc giả
- Xóa độc giả
- Tìm kiếm độc giả
- Xem lịch sử mượn sách của độc giả (kèm tiền phạt)

### 3. Mượn/Trả sách (📋)
- Tạo phiếu mượn (chọn độc giả + sách, tự động hạn trả 14 ngày)
- Kiểm tra số lượng sách: thông báo "Hết sách" nếu số lượng = 0
- Trả sách: tự động tính tiền phạt (2,000 VNĐ/ngày trễ hạn)
- Xem danh sách phiếu mượn với trạng thái (đang mượn/quá hạn/đã trả)
- Tìm kiếm phiếu mượn

## Cài đặt

### Yêu cầu
- Python 3.6 trở lên (Python 3.13 đã được kiểm tra)
- pip (Python package manager)

### Các bước cài đặt

1. **Clone repository**
   ```bash
   git clone https://github.com/Trwwngs1mp/Mini-Library-Management-System.git
   cd Mini-Library-Management-System
   ```

2. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**
   ```bash
   python web_app.py
   ```

4. **Mở trình duyệt**
   ```
   http://localhost:5000
   ```

## Cấu trúc thư mục

```
Mini-Library-Management-System/
├── web_app.py                   # Flask web application (REST API + Routes)
├── main.py                      # Desktop app entry point (Tkinter)
├── requirements.txt             # Python dependencies
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
│   └── view/                    # View - Desktop GUI (Tkinter)
│       ├── __init__.py
│       ├── main_window.py
│       ├── book_view.py
│       ├── reader_view.py
│       └── borrow_view.py
├── templates/                   # Jinja2 templates (Web)
│   ├── base.html                # Base layout with sidebar
│   ├── index.html               # Dashboard
│   ├── books.html               # Book management
│   ├── readers.html             # Reader management
│   └── borrow.html              # Borrow/Return management
├── static/
│   ├── css/
│   │   └── style.css            # Dark theme styles
│   └── js/
│       └── app.js               # JavaScript utilities
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

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/stats` | Thống kê tổng quan |
| GET | `/api/books?search=` | Danh sách sách |
| POST | `/api/books` | Thêm sách |
| PUT | `/api/books/:id` | Cập nhật sách |
| DELETE | `/api/books/:id` | Xóa sách |
| GET | `/api/readers?search=` | Danh sách độc giả |
| POST | `/api/readers` | Thêm độc giả |
| PUT | `/api/readers/:id` | Cập nhật độc giả |
| DELETE | `/api/readers/:id` | Xóa độc giả |
| GET | `/api/readers/:id/history` | Lịch sử mượn |
| GET | `/api/tickets?search=` | Danh sách phiếu mượn |
| POST | `/api/tickets/borrow` | Tạo phiếu mượn |
| POST | `/api/tickets/:id/return` | Trả sách |

## Tác giả

Bài tập môn: Lập trình giao diện và quản lý mã nguồn
