
from datetime import datetime, timedelta
from pathlib import Path
from core.member_base import Member
from core.book_model import Book 

class BookSearchMixin:
    def search_books(self):
        # Helper Function: A helper function to print book details in a visually appealing format with emojis and clear formatting for better user experience
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
    