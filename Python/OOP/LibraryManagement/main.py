from library import Library

def main():
    library = Library()

    while True:
        print("\nLibrary Menu:")
        print("1. Add User")
        print("2. Add Book")
        print("3. Lend Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Display Users")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter user name: ")
            library.add_user(name)

        elif choice == '2':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)

        elif choice == '3':
            user_id = int(input("Enter user ID: "))
            isbn = int(input("Enter book ISBN: "))
            library.lend_book(user_id, isbn)

        elif choice == '4':
            user_id = int(input("Enter user ID: "))
            isbn = int(input("Enter book ISBN: "))
            library.return_book(user_id, isbn)

        elif choice == '5':
            library.display_books()

        elif choice == '6':
            library.display_users()

        elif choice == '7':
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
