#!/usr/bin/env python3
"""
Library Management System (Python CLI)
Author: Hewad Rustom

Features:
- Add / list / search / update / delete books
- Borrow / return (availability + borrower name + dates)
- Persistent storage in library.json
- Simple, clean, menu-driven CLI
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

DB_FILE = "library.json"


# -------------------- storage --------------------
def load_db() -> Dict:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"books": [], "next_id": 1}


def save_db(db: Dict) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


# -------------------- helpers --------------------
def prompt(msg: str) -> str:
    return input(msg).strip()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def next_id(db: Dict) -> int:
    nid = db.get("next_id", 1)
    db["next_id"] = nid + 1
    return nid


def fmt_book(b: Dict) -> str:
    status = "AVAILABLE" if b["available"] else f"BORROWED by {b['borrower']}"
    return f"[{b['id']}] {b['title']} — {b['author']} ({b['year']})  :: {status}"


def find_by_id(db: Dict, bid: int) -> Optional[Dict]:
    for b in db["books"]:
        if b["id"] == bid:
            return b
    return None


# -------------------- actions --------------------
def add_book(db: Dict) -> None:
    print("\n➕ Add Book")
    title = prompt("Title: ")
    author = prompt("Author: ")
    year = prompt("Year (e.g., 2022): ")
    if not title or not author or not year:
        print("All fields are required.")
        return
    try:
        int(year)
    except ValueError:
        print("Year must be a number.")
        return

    book = {
        "id": next_id(db),
        "title": title,
        "author": author,
        "year": year,
        "available": True,
        "borrower": "",
        "borrowed_at": "",
        "returned_at": "",
        "created_at": now(),
        "updated_at": now(),
    }
    db["books"].append(book)
    save_db(db)
    print("✅ Book added.")


def list_books(db: Dict, only_available: bool = False) -> List[Dict]:
    items = db["books"]
    if only_available:
        items = [b for b in items if b["available"]]
    if not items:
        print("\n(No books found.)")
        return []
    print("\n📚 Books")
    print("-" * 72)
    for b in sorted(items, key=lambda x: (x["author"].lower(), x["title"].lower())):
        print(fmt_book(b))
    print("-" * 72)
    print(f"Total: {len(items)}")
    return items


def search_books(db: Dict) -> None:
    print("\n🔎 Search")
    q = prompt("Keyword (title/author): ").lower()
    if not q:
        print("Please enter a keyword.")
        return
    results = [
        b for b in db["books"]
        if q in b["title"].lower() or q in b["author"].lower()
    ]
    if not results:
        print("No matches.")
        return
    print(f"\nResults for '{q}':")
    for b in results:
        print(fmt_book(b))


def update_book(db: Dict) -> None:
    print("\n✏️  Update Book")
    try:
        bid = int(prompt("Enter book ID: "))
    except ValueError:
        print("Please enter a number.")
        return
    b = find_by_id(db, bid)
    if not b:
        print("ID not found.")
        return

    new_title = prompt(f"Title [{b['title']}]: ") or b["title"]
    new_author = prompt(f"Author [{b['author']}]: ") or b["author"]
    new_year = prompt(f"Year [{b['year']}]: ") or b["year"]
    if new_year and not new_year.isdigit():
        print("Year must be numeric.")
        return

    b["title"], b["author"], b["year"] = new_title, new_author, new_year
    b["updated_at"] = now()
    save_db(db)
    print("✅ Updated.")


def delete_book(db: Dict) -> None:
    print("\n🗑️  Delete Book")
    try:
        bid = int(prompt("Enter book ID: "))
    except ValueError:
        print("Please enter a number.")
        return
    before = len(db["books"])
    db["books"] = [b for b in db["books"] if b["id"] != bid]
    if len(db["books"]) < before:
        save_db(db)
        print("✅ Deleted.")
    else:
        print("ID not found.")


def borrow_book(db: Dict) -> None:
    print("\n📖 Borrow Book")
    try:
        bid = int(prompt("Enter book ID: "))
    except ValueError:
        print("Please enter a number.")
        return
    b = find_by_id(db, bid)
    if not b:
        print("ID not found.")
        return
    if not b["available"]:
        print(f"Already borrowed by {b['borrower']}.")
        return
    borrower = prompt("Borrower name: ")
    if not borrower:
        print("Borrower name required.")
        return
    b["available"] = False
    b["borrower"] = borrower
    b["borrowed_at"] = now()
    b["returned_at"] = ""
    b["updated_at"] = now()
    save_db(db)
    print("✅ Borrowed.")


def return_book(db: Dict) -> None:
    print("\n📦 Return Book")
    try:
        bid = int(prompt("Enter book ID: "))
    except ValueError:
        print("Please enter a number.")
        return
    b = find_by_id(db, bid)
    if not b:
        print("ID not found.")
        return
    if b["available"]:
        print("This book is already available.")
        return
    b["available"] = True
    b["returned_at"] = now()
    b["borrower"] = ""
    b["updated_at"] = now()
    save_db(db)
    print("✅ Returned.")


def stats(db: Dict) -> None:
    total = len(db["books"])
    available = len([b for b in db["books"] if b["available"]])
    borrowed = total - available
    print("\n📊 Stats")
    print(f"   Total books : {total}")
    print(f"   Available   : {available}")
    print(f"   Borrowed    : {borrowed}")


# -------------------- cli --------------------
def menu() -> str:
    print("\n=== Library CLI ===")
    print("1) Add book")
    print("2) List all books")
    print("3) List available books")
    print("4) Search books")
    print("5) Update a book")
    print("6) Delete a book")
    print("7) Borrow a book")
    print("8) Return a book")
    print("9) Stats")
    print("0) Exit")
    return input("Choose: ").strip()


def main():
    print("Welcome to Library Management CLI")
    db = load_db()
    while True:
        choice = menu()
        if choice == "1": add_book(db)
        elif choice == "2": list_books(db, only_available=False)
        elif choice == "3": list_books(db, only_available=True)
        elif choice == "4": search_books(db)
        elif choice == "5": update_book(db)
        elif choice == "6": delete_book(db)
        elif choice == "7": borrow_book(db)
        elif choice == "8": return_book(db)
        elif choice == "9": stats(db)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
