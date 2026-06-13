#!/usr/bin/env python3
"""
Seed script - Add sample data for demonstration.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model.database import Database
from src.controller.book_controller import BookController
from src.controller.reader_controller import ReaderController

db = Database()
book_controller = BookController(db)
reader_controller = ReaderController(db)

# Sample books with cover images from the web
sample_books = [
    {
        "title": "Harry Potter và Hòn đá Phù thủy",
        "author": "J.K. Rowling",
        "isbn": "978-0-7475-3269-9",
        "published_year": "1997",
        "quantity": 5,
    },
    {
        "title": "Nhà giả kim",
        "author": "Paulo Coelho",
        "isbn": "978-0-06-250217-4",
        "published_year": "1988",
        "quantity": 3,
    },
    {
        "title": "Chiến tranh và Hòa bình",
        "author": "Leo Tolstoy",
        "isbn": "978-0-19-923276-5",
        "published_year": "1869",
        "quantity": 2,
    },
    {
        "title": "Tôi thấy hoa vàng trên cỏ xanh",
        "author": "Nguyễn Nhật Ánh",
        "isbn": "978-604-1-08520-3",
        "published_year": "2010",
        "quantity": 4,
    },
    {
        "title": "Đắc nhân tâm",
        "author": "Dale Carnegie",
        "isbn": "978-0-671-02703-4",
        "published_year": "1936",
        "quantity": 6,
    },
    {
        "title": "Số đỏ",
        "author": "Vũ Trọng Phụng",
        "isbn": "978-604-69-1234-5",
        "published_year": "1936",
        "quantity": 3,
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0-13-235088-4",
        "published_year": "2008",
        "quantity": 2,
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "978-0-452-28423-4",
        "published_year": "1949",
        "quantity": 4,
    },
]

sample_readers = [
    {"name": "Nguyễn Văn An", "email": "nguyenvanan@gmail.com", "phone": "0901234567"},
    {"name": "Trần Thị Bình", "email": "tranthibinh@gmail.com", "phone": "0902345678"},
    {"name": "Lê Văn Cường", "email": "levancuong@yahoo.com", "phone": "0903456789"},
    {"name": "Phạm Thị Dung", "email": "phamthidung@outlook.com", "phone": "0904567890"},
    {"name": "Hoàng Văn Em", "email": "hoangvanem@gmail.com", "phone": "0905678901"},
]


def seed():
    print("🌱 Adding sample books...")
    for book in sample_books:
        result = book_controller.add_book(
            title=book["title"],
            author=book["author"],
            isbn=book["isbn"],
            published_year=book["published_year"],
            quantity=str(book["quantity"]),
        )
        if result["success"]:
            print(f"  ✅ {book['title']}")
        else:
            print(f"  ❌ {book['title']}: {result['errors']}")

    print("\n👤 Adding sample readers...")
    for reader in sample_readers:
        result = reader_controller.add_reader(
            name=reader["name"],
            email=reader["email"],
            phone=reader["phone"],
        )
        if result["success"]:
            print(f"  ✅ {reader['name']}")
        else:
            print(f"  ❌ {reader['name']}: {result['errors']}")

    print("\n✅ Seed data added successfully!")
    print(f"   📚 {len(sample_books)} books")
    print(f"   👤 {len(sample_readers)} readers")
    db.close()


if __name__ == "__main__":
    seed()