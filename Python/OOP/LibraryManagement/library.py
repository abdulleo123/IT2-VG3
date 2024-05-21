import csv
import random

class Book:
    def __init__(self, isbn, title, author, available=True):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = available

    def __str__(self):
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, {'Available' if self.available else 'Not Available'}"


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}"


class Library:
    def __init__(self, data_file="library_data.csv"):
        self.data_file = data_file
        self.users, self.books = self.load_data()

    def load_data(self):
        users = []
        books = []
        try:
            with open(self.data_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['type'] == 'user':
                        users.append(User(int(row['id']), row['name']))
                    elif row['type'] == 'book':
                        books.append(Book(int(row['id']), row['title'], row['author'], row['available'] == 'True'))
        except FileNotFoundError:
            pass
        return users, books

    def save_data(self):
        with open(self.data_file, mode='w', newline='') as file:
            fieldnames = ['type', 'id', 'name', 'title', 'author', 'available']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self.users:
                writer.writerow({'type': 'user', 'id': user.user_id, 'name': user.name})
            for book in self.books:
                writer.writerow({'type': 'book', 'id': book.isbn, 'title': book.title, 'author': book.author, 'available': 'True' if book.available else 'False'})

    def add_user(self, name):
        user_id = random.randint(1000, 9999)  # Generating a random 4-digit number as the user ID
        user = User(user_id, name)
        self.users.append(user)
        self.save_data()
        print(f"User '{name}' added to the library.")

    def add_book(self, title, author):
        isbn = random.randint(1000, 9999)  # Generating a random 4-digit number as the ISBN
        book = Book(isbn, title, author)
        self.books.append(book)
        self.save_data()
        print(f"Book '{title}' added to the library.")

    def lend_book(self, user_id, isbn):
        user = next((u for u in self.users if u.user_id == user_id), None)
        book = next((b for b in self.books if b.isbn == isbn), None)

        if user and book:
            if book.available:
                book.available = False
                self.save_data()
                print(f"Book '{book.title}' has been borrowed by {user.name}.")
            else:
                print(f"Book '{book.title}' is not available.")
        else:
            print("User ID or Book ISBN not found.")

    def return_book(self, user_id, isbn):
        user = next((u for u in self.users if u.user_id == user_id), None)
        book = next((b for b in self.books if b.isbn == isbn), None)

        if user and book:
            if not book.available:
                book.available = True
                self.save_data()
                print(f"Book '{book.title}' has been returned by {user.name}.")
            else:
                print(f"Book '{book.title}' was not borrowed.")
        else:
            print("User ID or Book ISBN not found.")

    def display_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            for book in self.books:
                print(book)

    def display_users(self):
        if not self.users:
            print("No users registered in the library.")
        else:
            for user in self.users:
                print(user)
