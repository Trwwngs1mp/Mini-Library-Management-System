#!/usr/bin/env python3
"""
Mini Library Management System - Web Application (Flask)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, send_from_directory
from src.model.database import Database
from src.controller.book_controller import BookController
from src.controller.reader_controller import ReaderController
from src.controller.borrow_controller import BorrowController

app = Flask(__name__)
app.config["SECRET_KEY"] = "mini-library-secret-key-2024"

# Initialize database and controllers
db = Database()
book_controller = BookController(db)
reader_controller = ReaderController(db)
borrow_controller = BorrowController(db)


# ---- Static files ----
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


# ---- Pages ----
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/books")
def books_page():
    return render_template("books.html")


@app.route("/readers")
def readers_page():
    return render_template("readers.html")


@app.route("/borrow")
def borrow_page():
    return render_template("borrow.html")


# ---- API: Books ----
@app.route("/api/books", methods=["GET"])
def api_get_books():
    keyword = request.args.get("search", "")
    books = book_controller.search_books(keyword)
    return jsonify(books)


@app.route("/api/books/<int:book_id>", methods=["GET"])
def api_get_book(book_id):
    book = book_controller.get_book_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books", methods=["POST"])
def api_add_book():
    data = request.get_json()
    result = book_controller.add_book(
        data.get("title", ""),
        data.get("author", ""),
        data.get("isbn", ""),
        data.get("published_year", ""),
        data.get("quantity", "1"),
        data.get("image_url", ""),
    )
    if result["success"]:
        return jsonify({"message": "Book added", "book_id": result["book_id"]}), 201
    return jsonify({"error": "\n".join(result["errors"])}), 400


@app.route("/api/books/<int:book_id>", methods=["PUT"])
def api_update_book(book_id):
    data = request.get_json()
    result = book_controller.update_book(
        book_id,
        data.get("title", ""),
        data.get("author", ""),
        data.get("isbn", ""),
        data.get("published_year", ""),
        data.get("quantity", "1"),
        data.get("image_url", ""),
    )
    if result["success"]:
        return jsonify({"message": "Book updated"})
    return jsonify({"error": "\n".join(result["errors"])}), 400


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def api_delete_book(book_id):
    result = book_controller.delete_book(book_id)
    if result["success"]:
        return jsonify({"message": "Book deleted"})
    return jsonify({"error": "\n".join(result["errors"])}), 400


# ---- API: Readers ----
@app.route("/api/readers", methods=["GET"])
def api_get_readers():
    keyword = request.args.get("search", "")
    readers = reader_controller.search_readers(keyword)
    return jsonify(readers)


@app.route("/api/readers/<int:reader_id>", methods=["GET"])
def api_get_reader(reader_id):
    reader = reader_controller.get_reader_by_id(reader_id)
    if reader:
        return jsonify(reader)
    return jsonify({"error": "Reader not found"}), 404


@app.route("/api/readers", methods=["POST"])
def api_add_reader():
    data = request.get_json()
    result = reader_controller.add_reader(
        data.get("name", ""),
        data.get("email", ""),
        data.get("phone", ""),
    )
    if result["success"]:
        return jsonify({"message": "Reader added", "reader_id": result["reader_id"]}), 201
    return jsonify({"error": "\n".join(result["errors"])}), 400


@app.route("/api/readers/<int:reader_id>", methods=["PUT"])
def api_update_reader(reader_id):
    data = request.get_json()
    result = reader_controller.update_reader(
        reader_id,
        data.get("name", ""),
        data.get("email", ""),
        data.get("phone", ""),
    )
    if result["success"]:
        return jsonify({"message": "Reader updated"})
    return jsonify({"error": "\n".join(result["errors"])}), 400


@app.route("/api/readers/<int:reader_id>", methods=["DELETE"])
def api_delete_reader(reader_id):
    result = reader_controller.delete_reader(reader_id)
    if result["success"]:
        return jsonify({"message": "Reader deleted"})
    return jsonify({"error": "\n".join(result["errors"])}), 400


@app.route("/api/readers/<int:reader_id>/history", methods=["GET"])
def api_reader_history(reader_id):
    history = reader_controller.get_borrow_history(reader_id)
    return jsonify(history)


# ---- API: Borrow Tickets ----
@app.route("/api/tickets", methods=["GET"])
def api_get_tickets():
    keyword = request.args.get("search", "")
    tickets = borrow_controller.search_tickets(keyword)
    return jsonify(tickets)


@app.route("/api/tickets/<int:ticket_id>", methods=["GET"])
def api_get_ticket(ticket_id):
    ticket = borrow_controller.get_ticket_by_id(ticket_id)
    if ticket:
        return jsonify(ticket)
    return jsonify({"error": "Ticket not found"}), 404


@app.route("/api/tickets/borrow", methods=["POST"])
def api_borrow_book():
    data = request.get_json()
    result = borrow_controller.create_borrow(
        data.get("reader_id"), data.get("book_id")
    )
    if result["success"]:
        return jsonify({"message": "Borrowed", "ticket_id": result["ticket_id"]}), 201
    return jsonify({"error": "\n".join(result["errors"])}), 400


@app.route("/api/tickets/<int:ticket_id>/return", methods=["POST"])
def api_return_book(ticket_id):
    result = borrow_controller.return_book(ticket_id)
    if result["success"]:
        return jsonify({"message": "Returned", "fine": result["fine"]})
    return jsonify({"error": "\n".join(result["errors"])}), 400


# ---- API: Stats ----
@app.route("/api/stats", methods=["GET"])
def api_stats():
    books = book_controller.get_all_books()
    readers = reader_controller.get_all_readers()
    active_tickets = borrow_controller.get_active_tickets()
    total_tickets = borrow_controller.get_all_tickets()
    total_fine = sum(t.get("fine", 0) or 0 for t in total_tickets)
    return jsonify({
        "total_books": len(books),
        "total_readers": len(readers),
        "active_borrows": len(active_tickets),
        "total_fine": total_fine,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)