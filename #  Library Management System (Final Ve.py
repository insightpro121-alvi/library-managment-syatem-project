#  Library Management System 
#  Features:
# - User login (asks User ID first)
#  total books, available, borrowed, total users
# - Multiple copies  ha same book
#  library.txt stores all data

import os

# ------------------ FILE HANDLING ------------------
def save_all_data(books, users, filename):
    """Save both books and users to one file"""
    try:
        with open(filename, "w") as f:
            f.write("#BOOKS\n")
            for book_id, b in books.items():
                f.write(f"{book_id},{b['Title']},{b['Author']},{b['Year']},{b['TotalCopies']},{b['AvailableCopies']},{b['BorrowedBy']}\n")
            f.write("#USERS\n")
            for user_id, u in users.items():
                borrowed = ";".join(u["BorrowedBooks"]) if u["BorrowedBooks"] else "None"
                f.write(f"{user_id},{u['Name']},{u['Email']},{borrowed}\n")
        print(" All data saved successfully!")
    except Exception as e:
        print(f" Error saving data: {e}")


def load_all_data(filename):
    """Load books and users from one file"""
    books, users = {}, {}
    try:
        with open(filename, "r") as f:
            section = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == "#BOOKS":
                    section = "books"
                    continue
                elif line == "#USERS":
                    section = "users"
                    continue

                if section == "books":
                    parts = line.split(",")
                    if len(parts) < 7:
                        continue
                    book_id, title, author, year, total, available, borrowed_by = parts
                    books[book_id] = {
                        "Title": title,
                        "Author": author,
                        "Year": year,
                        "TotalCopies": int(total),
                        "AvailableCopies": int(available),
                        "BorrowedBy": borrowed_by
                    }
                elif section == "users":
                    parts = line.split(",")
                    if len(parts) < 4:
                        continue
                    user_id, name, email, borrowed_books = parts
                    borrowed_list = borrowed_books.split(";") if borrowed_books != "None" else []
                    users[user_id] = {
                        "Name": name,
                        "Email": email,
                        "BorrowedBooks": borrowed_list
                    }
        print(" Data loaded successfully!")
    except FileNotFoundError:
        print(" No file found — starting fresh.")
    return books, users


# ------------------ DASHBOARD ------------------
def show_dashboard(books, users):
    total_books = len(books)
    total_users = len(users)
    available = sum(b["AvailableCopies"] for b in books.values())
    borrowed = sum((b["TotalCopies"] - b["AvailableCopies"]) for b in books.values())

    print("\n" + "="*60)
    print(" LIBRARY DASHBOARD")
    print("="*60)
    print(f" Total Books: {total_books}")
    print(f" Available Copies: {available}")
    print(f" Borrowed Copies: {borrowed}")
    print(f" Total Users: {total_users}")
    print("="*60)


# ------------------ BOOK FUNCTIONS -------------------- jango mango
def add_book(books, filename, users):
    """Add new book or increase copies"""
    while True:
        book_id = input("Enter Book ID: ")
        if book_id in books:
            print("Book already exists — adding more copies.")
            extra = int(input("How many extra copies to add? "))
            books[book_id]["TotalCopies"] += extra
            books[book_id]["AvailableCopies"] += extra
        else:
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            year = input("Enter Published Year: ")
            copies = int(input("Enter Number of Copies: "))
            books[book_id] = {
                "Title": title,
                "Author": author,
                "Year": year,
                "TotalCopies": copies,
                "AvailableCopies": copies,
                "BorrowedBy": "None"
            }
        save_all_data(books, users, filename)
        print(" Book record updated successfully!")
        if input("Add another book? (y/n): ").lower() != 'y':
            break


def show_available_books(books):
    """Show books that have at least one available copy"""
    print("\n AVAILABLE BOOKS")
    print("="*60)
    found = False
    for b in books.values():
        if b["AvailableCopies"] > 0:
            found = True
            print(f"{b['Title']} by {b['Author']} ({b['Year']}) — {b['AvailableCopies']} copies available")
    if not found:
        print(" No books currently available.")
    print("="*60)


def display_all_books(books):
    """Show all books"""
    print("="*60)
    if not books:
        print("No books found.")
        return
    for book_id, b in books.items():
        print(f"[{book_id}] {b['Title']} by {b['Author']} ({b['Year']})")
        print(f"   Total: {b['TotalCopies']} | Available: {b['AvailableCopies']} | Borrowed by: {b['BorrowedBy']}")
    print("="*60)


# ------------------ USER FUNCTIONS ------------------
def user_login(users, filename, books):
    """Ask user to log in or create new account"""
    user_id = input("Enter your User ID: ")
    if user_id in users:
        print(f"Welcome back, {users[user_id]['Name']}!")
    else:
        print("New user detected — please register.")
        name = input("Enter your Name: ")
        email = input("Enter your Email: ")
        users[user_id] = {"Name": name, "Email": email, "BorrowedBooks": []}
        save_all_data(books, users, filename)
        print(" User registered successfully!")
    return user_id


def display_users(users):
    """Show all registered users"""
    print("\n ALL USERS")
    print("="*60)
    for user_id, u in users.items():
        borrowed = ", ".join(u["BorrowedBooks"]) if u["BorrowedBooks"] else "None"
        print(f"[{user_id}] {u['Name']} ({u['Email']}) | Borrowed: {borrowed}")
    print("="*60)


# ------------------ TRANSACTIONS ------------------
def borrow_book(books, users, filename, current_user):
    book_id = input("Enter Book ID to borrow: ")
    if book_id not in books:
        print(" Book not found.")
        return
    book = books[book_id]
    if book["AvailableCopies"] <= 0:
        print(" No copies available right now.")
        return

    users[current_user]["BorrowedBooks"].append(book_id)
    book["AvailableCopies"] -= 1
    book["BorrowedBy"] = current_user
    save_all_data(books, users, filename)
    print(f" You borrowed '{book['Title']}' successfully!")


def return_book(books, users, filename, current_user):
    book_id = input("Enter Book ID to return: ")
    if book_id not in users[current_user]["BorrowedBooks"]:
        print(" You haven’t borrowed this book.")
        return
    users[current_user]["BorrowedBooks"].remove(book_id)
    books[book_id]["AvailableCopies"] += 1
    books[book_id]["BorrowedBy"] = "None"
    save_all_data(books, users, filename)
    print(f" You returned '{books[book_id]['Title']}' successfully!")


# ------------------ MAIN ------------------
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "library.txt")
    books, users = load_all_data(filename)

    current_user = user_login(users, filename, books)

    while True:
        show_dashboard(books, users)
        print("\n MAIN MENU")
        print("="*60)
        print("1. Add Book")
        print("2. Display All Books")
        print("3. Show Available Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Display All Users")
        print("7. Exit")
        print("="*60)

        choice = input("Enter choice: ")
        if choice == '1':
            add_book(books, filename, users)
        elif choice == '2':
            display_all_books(books)
        elif choice == '3':
            show_available_books(books)
        elif choice == '4':
            borrow_book(books, users, filename, current_user)
        elif choice == '5':
            return_book(books, users, filename, current_user)
        elif choice == '6':
            display_users(users)
        elif choice == '7':
            save_all_data(books, users, filename)
            print(" Data saved. Exiting... Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
