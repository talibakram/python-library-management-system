
from datetime import datetime, timedelta
from pathlib import Path
from core.admin_base import Admin
from core.book_model import Book

class ManageBooksMixin:
    def view_all_books(self):
        def print_vip_format(books_list):
            for book in books_list:
                print("-" * 55)
                print(f"📖 Title     : {book.get('Title', 'Unknown')}")
                print(f"🔑 Book-ID   : {book.get('Book-ID', 'Unknown')}")
                print(f"✍️  Author    : {book.get('Author', 'Unknown')}")
                print(f"📚 Category  : {book.get('Category', 'Unknown')}")
                print(f"📦 Available : {book.get('Available', 0)} copies remaining")
            print("-" * 55)

        while True:
            print("\n" + "="*50)
            print(" "*16 + "🔍 SEARCH BOOKS 🔍")
            print("="*50)
            print("Search books by:")
            print("1. By Title")
            print("2. By Book-ID")
            print("3. By Author Name")
            print("4. By Category")
            print("5. View all available books")
            print("0. Go Back")
            print("="*50)

            while True:
                try:
                    choice = int(input("\nEnter your choice (0-5): "))
                    break
                except ValueError:
                    print("\nInvalid response! Please enter a number.\n")

            if choice == 0:
                break
                
            elif choice == 1:
                title = input("Enter book title (or part of it): ").strip().lower()
                # Smart Search: 'in' use kiya hy taake aadhi spelling se bhi kitab mil jaye
                title_check = [i for i in Book.book_data if title in i.get("Title", "").lower()]
                
                if len(title_check) == 0:
                    print("\nBook not found! Please check the spelling.\n")
                else:
                    print(f"\nFound {len(title_check)} book(s) matching your search:\n")
                    print_vip_format(title_check)
                input("Press enter to go back...\n")

            elif choice == 2:
                book_id = input("Enter exact Book-ID: ").strip()
                id_check = [i for i in Book.book_data if i.get("Book-ID") == book_id]
                
                if len(id_check) == 0:
                    print("\nBook not found! Invalid Book-ID.\n")
                else:
                    print("\nHere are the book details:\n")
                    print_vip_format(id_check)
                input("Press enter to go back...\n")

            elif choice == 3:
                author_name = input("Enter author name (or part of it): ").strip().lower()
                author_check = [i for i in Book.book_data if author_name in i.get("Author", "").lower()]
                
                if len(author_check) == 0:
                    print("\nNo books found by this author!\n")
                else:
                    print(f"\nFound {len(author_check)} book(s) by this author:\n")
                    print_vip_format(author_check)
                input("Press enter to go back...\n")

            elif choice == 4:
                category = input("Enter book category (e.g. Programming): ").strip().lower()
                category_check = [i for i in Book.book_data if category in i.get("Category", "").lower()]
                
                if len(category_check) == 0:
                    print("\nNo books found in this category!\n")
                else:
                    print(f"\nFound {len(category_check)} book(s) in '{category.title()}':\n")
                    print_vip_format(category_check)
                input("Press enter to go back...\n")

            elif choice == 5:
                print("\n" + "="*55)
                print(" "*12 + "📚 ALL AVAILABLE LIBRARY BOOKS 📚")
                print("="*55)
                
                if len(Book.book_data) == 0:
                    print("\nLibrary is currently empty!\n")
                else:
                    print_vip_format(Book.book_data)
                input("Press enter to go back...\n")
                
            else:
                print("\nInvalid choice! Please select an option between 0 and 5.\n")
        

    def update_book_details(self):
        while True:
            print("Update Book Details:\n")
            print("1. Update Book Title")
            print("2. Update Author Name")
            print("3. Update Book Category")
            print("4. Update Book Status")
            print("0. Back")
            while True:
                try:
                    choice = int(input("Enter your response: "))
                except ValueError:
                    print("\nResponse must be i digits\n")
                    continue
                break
            if choice == 0:
                break
            elif choice == 1:
                while True:
                    book_id = input("Enter Book-ID: ")
                    id_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(id_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break
                new_title = input("Enter new title: ").strip().title()
                id_check[0]["Title"] = new_title
                Book.update()
                print(f"\nBook title updated to {new_title}.\n")
                input("Press enter to go back...\n")
            elif choice == 2:
                while True:
                    book_id = input("Enter Book-ID: ")
                    id_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(id_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break
                new_author = input("Enter new author: ").strip().title()
                id_check[0]["Author"] = new_author
                Book.update()
                print(f"\nAuthor name updated to {new_author}.\n")
                input("Press enter to go back...\n")
            elif choice == 3:
                while True:
                    book_id = input("Enter Book-ID: ")
                    id_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(id_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break
                new_category = input("Enter new category: ").strip().title()
                id_check[0]["Category"] = new_category
                Book.update()
                print(f"\nBook category updated to {new_category}.\n")
                input("Press enter to go back...\n")
            elif choice == 4:
                while True:
                    book_id = input("Enter Book-ID: ")
                    id_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(id_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break
                new_status = input("Enter new status: ").strip().title()
                id_check[0]["Status"] = new_status
                Book.update()
                print(f"\nBook status updated to {new_status}.\n")
                input("Press enter to go back...\n")
            else:
                print("\nInvalid response! Try Again.\n")

    def delete_book(self):
        print("\nDelete book:\n")
        while True:
            book_id = input("Enter Book-ID to delete book: ")
            id_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
            if len(id_check) == 0:
                print("\nBook not found!\n")
                continue
            break
        index = Book.book_data.index(id_check[0])
        Book.book_data.pop(index)
        Book.update()
        print(f"\nBook [{id_check[0]["Title"]}] deleted successfully.\n")
        input("Press enter to go back...\n")

    def manage_categories(self):
        while True:
            print("1. Delete Category")
            print("2. Rename Category")
            print("3. View All Categories")
            print("0. Back")
            while True:
                try:
                    choice = int(input("Enter your response: "))
                except ValueError:
                    print("\nResponse must be in digits!\n")
                    continue
                break
            if choice == 0:
                break
            elif choice == 1:
                while True:
                    book_category = (
                        input("Enter Book Category you want to delete: ")
                        .strip()
                        .title()
                    )
                    category_check = [
                        i for i in Book.book_data if i["Category"] == book_category
                    ]
                    if len(category_check) == 0:
                        print("\nCategory not found!\n")
                        continue
                    for i in category_check:
                        i["Category"] = "Uncatrgorized"
                    Book.update()
                    print(f"\nCategory '{book_category}' deleted!\n")
                    print(f"{len(category_check)} book(s) moved to 'Uncategorized'.\n")
                    break
            elif choice == 2:
                while True:
                    book_category = (
                        input("Enter book category yo want to rename: ").strip().title()
                    )
                    category_check = [
                        i for i in Book.book_data if i["Category"] == book_category
                    ]
                    if len(category_check) == 0:
                        print("\nCategory not found!\n")
                        continue
                    new_category = input("Enter new category name: ").strip().title()
                    for i in category_check:
                        i["Category"] = new_category
                    Book.update()
                    print(
                        f"\nCategory '{book_category}' successfully renamed to '{new_category}'.\n"
                    )
                    print(
                        f"'{len(category_check)}' Categories renamed to '{new_category}'.\n"
                    )
                    break
            elif choice == 3:
                num = 1
                book_categories = [i for i in Book.book_data]
                print("All categories:\n")
                for i in book_categories:
                    print(f"{num}. {i["Category"]}")
                    num += 1
                input("\nPress Enter to go back...\n")
            else:
                print("\nInvalid response! Try again.\n")
