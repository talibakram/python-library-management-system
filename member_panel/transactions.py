
import random
from datetime import datetime, timedelta
from pathlib import Path
from core.member_base import Member
from core.book_model import Book

class MemberTransactionsMixin:
    def reserve_book(self):
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\n❌ CRITICAL ERROR: No active session found. Please login again.\n")
            return
        user = self.current_user
        while True:
            print("\n" + "="*50)
            print(" "*16 + "BOOK RESERVATION")
            print("="*50)
            print("1. Reserve a book")
            print("2. View my reserved books")
            print("3. Cancel a reservation")
            print("0. Go Back")
            print("="*50)

            while True:
                try:
                    choice = int(input("\nEnter your choice: "))
                except ValueError:
                    print("\nInvalid input! Please enter a number.\n")
                    continue
                break
            if choice == 0:
                break
            elif choice == 1:
                # Check if the user is blocked or restricted
                if user.get("Status") in ["Blocked", "Restricted"]:
                    print("\nYou are blocked/restricted and cannot reserve books!\n")
                    input("Press enter to go back...\n")
                    continue
                # Check if the user has reserved 3 or more books 
                if len(user.get("Reserved Books", [])) >= 3:
                    print("\nYou have reached the maximum reservation limit (3 books)!")
                    print("Cancel an old reservation first to reserve a new one.\n")
                    input("Press enter to go back...\n")
                    continue
                # Check if the user has issued 3 or more books
                if len(user.get("Issued Books", [])) >= 3:
                    print("\nYou have already issued 3 books! Return a book first to reserve a new one.\n")
                    input("Press enter to go back...\n")
                    continue
                
                while True:
                    book_id = input("Enter Book-ID: ").strip()
                    book_check = [i for i in Book.book_data if i.get("Book-ID") == book_id]
                    if len(book_check) == 0:
                        print("\nBook not found! Please check the Book-ID.\n")
                        continue
                    break

                target_book = book_check[0]

                # Check if book is available for issue, if yes then no need to reserve
                if target_book.get("Status") == "Available" or target_book.get("Available", 0) > 0:
                    print("\nThis book is currently available in the library. No need to reserve, you can issue it directly!\n")
                    input("Press enter to go back...\n")
                    continue

                
                # VIP FIX: To prevent KeyError Bomb initialized list
                target_book.setdefault("Reserved-By", [])

                # Check if member has already reserved this book, if yes then do not allow to reserve again
                already_reserved = any(res.get("Member-ID") == user.get("Member-ID") for res in target_book["Reserved-By"])
                if already_reserved:
                    print("\nYou have already reserved this book!\n")
                    input("Press enter to go back...\n")
                    continue

                # Check if member has already issued this book and not returned yet, if yes then do not allow to reserve again
                already_issued = any(
                    (record.get("Book-ID") == book_id and record.get("Return Status") == "Pending") 
                    for record in user.get("Issued Books", [])
                )
                
                if already_issued:
                    print("\n❌ ERROR: You already have this book issued right now! Return it first to reserve.\n")
                    input("Press enter to go back...\n")
                    continue

                # Add reservation record to book's reserved-by list
                date = datetime.today().strftime("%d-%m-%Y")
                target_book["Reserved-By"].append({
                        "Member-ID": user["Member-ID"],
                        "Name": user["Name"], 
                        "Reserve Date": date
                    })

                # Add reservation record to member's reserved books list
                user.setdefault("Reserved Books", []).append({
                    "Book-ID": book_id,
                    "Title": target_book.get("Title", "Unknown"),
                    "Reserve Date": date
                })

                # Update JSON files
                Book.update()
                Member.update()

                print(f"\nSUCCESS! '{target_book.get('Title', 'Book')}' has been reserved successfully for you.\n")
                input("Press enter to go back...\n")

            elif choice == 2:
                res_books = user.get("Reserved Books", [])
                if len(res_books) == 0:
                    print("\nYou do not have any reservation yet.\n")
                else:
                    print("\n" + "="*50)
                    print(f" "*12 + f"--RESERVATIONS FOR {user.get('Name', 'USER').upper()}--")
                    print("="*50)
                    for idx, res in enumerate(res_books, 1):
                        
                        book_id = res.get('Book-ID', 'N/A')
                        title = res.get('Title', 'Unknown')
                        date = res.get('Reserve Date', 'Unknown')
                        
                        print(f"{idx}. Book-ID: {book_id} | Title: {title} | Date: {date}")
                        
                    print("="*50 + "\n")
                    input("Press enter to go back...\n")

            elif choice == 3:
                res_books = user.get("Reserved Books", [])
                if len(res_books) == 0:
                    print("\nYou do not have any reservation yet.\n")
                    input("Press enter to go back...\n")

                else:
                    while True:
                        book_id = input("Enter Book-ID: ").strip()
                        book_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                        if len(book_check) == 0:
                            print("\nBook not found!\n")
                            continue
                        break
                    # Check if reservation exists, if yes then cancel reservation
                    res_exists = any(res["Book-ID"] == book_id for res in user["Reserved Books"])
                    
                    if not res_exists:
                        print("\nNo such reservation found for book!\n")
                        continue
                    
                    # Remove member from book's reserved-by list 
                    # Remove book from member's reserved books list
                    book_check[0]["Reserved-By"] = [res for res in book_check[0]["Reserved-By"] if res["Member-ID"] != user["Member-ID"]]
                    user["Reserved Books"] = [res for res in user["Reserved Books"] if res["Book-ID"] != book_id]

                    Member.update()
                    Book.update()
                    print(f"\nSUCCESS: Reservation for Book '{book_id}' has been canceled.\n")
                    input("Press enter to go back...\n")

            else:
                print("\nInvalid choice! Try again.\n")

    def issue_book(self):
        # Checking the current user loged in or not
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\n❌ CRITICAL ERROR: No active session found. Please login again.\n")
            return
        user = self.current_user

        if user.get("Status") in ["Blocked", "Restricted"]:
            print("\nYou are blocked/restricted and cannot issue books!\n")
            input("Press enter to go back...\n")
            return
        
        if len(user.get("Issued Books", [])) >= 3:
            # Fixed Copy-Paste text
            print("\nYou have already issued 3 books! Return a book first to issue a new one.\n")
            input("Press enter to go back...\n")
            return

        print("\n" + "="*50)
        print(" "*16 + "ISSUE BOOK")
        print("="*50)

        while True:
            book_id = input("Enter Book-ID: ").strip()
            # .get() use kiya taake KeyError na aaye
            id_check = [i for i in Book.book_data if i.get("Book-ID") == book_id]
            
            if len(id_check) == 0:
                print("\nBook not found! Please check ID.\n")
                continue
                
            target_book = id_check[0]

            if (
                target_book.get("Status") == "Out Of Stock"
                or target_book.get("Total Copies", 0) == target_book.get("Issued", 0)
                or target_book.get("Available", 0) <= 0
            ):
                print("\nBook is currently out of stock or all copies are issued!\n")
                input("Press enter to go back...\n")
                return
            break

        # VIP FIX: To prevent KeyError Bomb initialized lists
        target_book.setdefault("Reserved-By", [])
        target_book.setdefault("Issued-To", [])
        user.setdefault("Issued Books", [])

        # VIP Reservation Logic Fix:
        # Check if anyone else has reserved this book and no extra copies are available
        is_reserved_by_me = any(res.get("Member-ID") == user.get("Member-ID") for res in target_book["Reserved-By"])
        total_reservations = len(target_book["Reserved-By"])
        
        if not is_reserved_by_me and target_book.get("Available", 0) <= total_reservations:
            print("\nThis book is reserved by another member and no extra copies are available!\n")
            input("Press enter to go back...\n")
            return

        # Check if member has already issued this book
        already_issued = any(
            (record.get("Book-ID") == book_id and record.get("Return Status") == "Pending") 
            for record in user["Issued Books"]
        )
                
        if already_issued:
            print("\nERROR: You already have this book issued right now! Return it first.\n")
            input("Press enter to go back...\n")
            return
        
        issue_date_obj = datetime.today()
        due_date_obj = issue_date_obj + timedelta(days=7)
        issue_date_str = issue_date_obj.strftime("%d-%m-%Y")
        due_date_str = due_date_obj.strftime("%d-%m-%Y")
        trx_id = f"TRX.{random.randint(10000,99999)}"
        record = {
            "Transaction-ID": trx_id,
            "Book-ID": book_id,
            "Title": id_check[0]["Title"],
            "Issue Date": issue_date_str,
            "Due Date": due_date_str,
            "Return Date": "Not Returned",
            "Late Days": 0,
            "Fine Amount": 0,
            "Return Status": "Pending",
        }
        record2 = {
            "Member-ID": user["Member-ID"],
            "Name": user["Name"],
            "Transaction-ID": trx_id,
            "Issue Date": issue_date_str,
            "Due Date": due_date_str,
        }
        # Updating Database
        user["Issued Books"].append(record)
        target_book["Issued-To"].append(record2)
        
        target_book["Available"] -= 1
        target_book["Issued"] += 1
        Member.update()
        Book.update()

        # After issueing, check the available copies update "Status" as "Issued" if available copies equals to 0. 
        if target_book["Available"] == 0:
            target_book["Status"] = "Issued"

        # If the member had reserved this book, then remove from the reservation list of book
        if is_reserved_by_me:
            target_book["Reserved-By"] = [res for res in target_book["Reserved-By"] if res.get("Member-ID") != user.get("Member-ID")]

            # ALso remove from the member's reserved books' list
            if "Reserved Books" in user:
                 user["Reserved Books"] = [b for b in user["Reserved Books"] if b.get("Book-ID") != book_id]

        Book.update()
        Member.update()

        print(f"\nBook issued successfully to {user['Name']}. Your Transaction-ID is {trx_id}.\n")
        print(f"Please return it by: {due_date_str}\n")
        input("Press enter to go back...\n")


    def return_book(self):
        # Checking the current user loged in or not
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\nCRITICAL ERROR: No active session found. Please login again.\n")
            return
        user = self.current_user

        print("\n" + "="*50)
        print(" "*16 + "RETURN BOOK")
        print("="*50)

        while True:
            book_id = input("Enter Book-ID you want to return: ").strip()
        
            book_check = [i for i in Book.book_data if i.get("Book-ID") == book_id]
            
            if len(book_check) == 0:
                print("\nBook not found in library records!\n")
                continue
            break
            
        target_book = book_check[0]
        book_found = False

        for book in user.get("Issued Books", []):
            if book.get("Book-ID") == book_id and book.get("Return Status") == "Pending":
                book_found = True

                # Calculate late days and fine amount
                due_date_str = book.get("Due Date")
                try:
                    due_date_obj = datetime.strptime(due_date_str, "%d-%m-%Y")
                    today_date = datetime.today()
                    late_days = (today_date - due_date_obj).days  # Calculate late days
                except (ValueError, TypeError):
                    late_days = 0 # Failsafe in case date is missing or corrupt

                if late_days > 0:
                    fine_amount = late_days * 50
                    book["Late Days"] = late_days
                    book["Fine Amount"] = fine_amount

                    # Add fine in member's profile!
                    current_total_fine = user.get("Total Fine", 0)
                    user["Total Fine"] = current_total_fine + fine_amount
                    
                    print(f"\n⚠️ Late Return: You are late by {late_days} days!")
                    print(f"💸 Fine Added: RS. {fine_amount} to your account.\n")
                else:
                    book["Late Days"] = 0
                    book["Fine Amount"] = 0
                    print("\nBook returned on time. No fine added.")

                # Update return status and return date
                book["Return Status"] = "Returned"
                book["Return Date"] = datetime.today().strftime("%d-%m-%Y")
                break  # Break the loop once the book is found and processed

        if not book_found:
            print("\nThis book is not issued to you or has already been returned!\n")
            input("Press enter to go back...\n")
            return
        
        # Update book availability safely
        target_book["Available"] = target_book.get("Available", 0) + 1
        target_book["Issued"] = target_book.get("Issued", 1) - 1
        
        if target_book["Available"] > 0:
            target_book["Status"] = "Available"

        # Initialized lists to prevent keyErrors
        target_book.setdefault("Issued-To", [])
        target_book.setdefault("Reserved-By", [])
        user.setdefault("Reserved Books", [])

        target_book["Issued-To"] = [
            i for i in target_book["Issued-To"] if i.get("Member-ID") != user.get("Member-ID")
        ]

        # --- AUTO-DELETE RESERVATION LOGIC ---
        # 1. Delete member from book's reservation list
        target_book["Reserved-By"] = [
            res for res in target_book["Reserved-By"] if res.get("Member-ID") != user.get("Member-ID")
        ]
                
        # 2. Delete this book from member's reserved books list
        user["Reserved Books"] = [
            res for res in user["Reserved Books"] if res.get("Book-ID") != book_id
        ]

        # Update JSON files
        Book.update()
        Member.update()

        print(f"\nBook returned successfully. Thank you, {user.get('Name', 'Member')}!\n")
        input("Press enter to go back...\n")
