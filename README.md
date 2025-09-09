# 📚 Library Management System (Python CLI)

A simple, menu-driven **Library Management System** built in Python. It allows adding, updating, deleting, borrowing, and returning books, with persistent storage in `library.json`.

## 🚀 Features
- ➕ Add new books (title, author, year)
- 📖 Borrow & return books with borrower tracking
- 📝 Update or delete book records
- 🔎 Search by title or author
- 📚 List all books (or only available ones)
- 📊 Stats: total, available, borrowed
- 💾 Persistent storage in `library.json`

## 🛠️ How to Run
```bash
python library.py
📌 Example Run
pgsql
Copy code
Welcome to Library Management CLI

=== Library CLI ===
1) Add book
2) List all books
3) List available books
4) Search books
5) Update a book
6) Delete a book
7) Borrow a book
8) Return a book
9) Stats
0) Exit

Choose: 1
Title: The Pragmatic Programmer
Author: Andrew Hunt
Year: 1999
✅ Book added!
📖 What I Learned
Managing structured data with JSON

Designing CRUD operations in Python CLI

Tracking availability and borrowers

Writing modular, reusable functions

Building clean, interactive CLI apps
