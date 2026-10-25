
import random
from datetime import datetime, timedelta
from pathlib import Path
from core.admin_base import Admin
from core.member_base import Member
from core.book_model import Book

class AdminCirculationMixin:
    def issue_book(self):
        print("\nIssue A Book\n")
        while True:
            book_id = input("Enter Book-ID: ").strip()
            id_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
            if len(id_check) == 0:
                print("\nBook not found!\n")
                continue
            if (
                id_check[0]["Status"] == "Out Of Stock"
                or id_check[0]["Total Copies"] == id_check[0]["Issued"]
                or id_check[0]["Available"] == 0
            ):
                print("\nBook out of stock or issued!\n")
                input("Press enter to go back...\n")
                return
            break
        while True:
            member_id = input("\nEnter Member-ID: ").strip()
            username = input("Enter member's username: ").strip()
            info_check = [
                i
                for i in Member.member_data
                if i["Member-ID"] == member_id and i["Username"] == username
            ]
            if len(info_check) == 0:
                print("\nMember not found\n")
                continue
            if (
                info_check[0]["Status"] == "Blocked"
                or info_check[0]["Status"] == "Restricted"
            ):
                print("\nMember is blocked/restricted!\n")
                input("Press enter to go back...\n")
                return
            break
        already_issued = False
        for issued_items in info_check[0]["Issued Books"]:
            if book_id == issued_items["Book-ID"]:
                already_issued = True
                break
        if already_issued:
            print(f"\nThis book is already issued to {info_check[0]["Name"]}!\n")
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
            "Member-ID": member_id,
            "Name": info_check[0]["Name"],
            "Transaction-ID": trx_id,
            "Issue Date": issue_date_str,
            "Due Date": due_date_str,
        }
        info_check[0]["Issued Books"].append(record)
        Member.update()
        id_check[0]["Available"] -= 1
        id_check[0]["Issued"] += 1
        id_check[0]["Issued-To"].append(record2)
        Book.update()

        if id_check[0]["Available"] == 0:
            id_check[0]["Status"] = "Issued"
        elif id_check[0]["Available"] == 0 and id_check[0]["Total Copies"] == 0:
            id_check[0]["Available"] = "Out Of Stock"
            Book.update()
        print(f"\nBook issued successfully to {info_check[0]["Name"]}.\n")
        input("Press enter to go back...\n")

    def return_book(self):
        print("\n--- Return A Book ---\n")

        # 1. Member Verification
        while True:
            member_id = input("Enter Member-ID: ").strip()
            info_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
            if len(info_check) == 0:
                print("\nMember not found!\n")
                continue
            break
        # 2. Book Verification
        while True:
            book_id = input("Enter Book-ID: ").strip()
            book_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
            if len(book_check) == 0:
                print("\nBook not found!\n")
                continue
            break
        book_found = False
        for book in info_check[0]["Issued Books"]:
            if book["Book-ID"] == book_id and book["Return Status"] == "Pending":
                book_found = True

                # Calculate late days and fine amount
                due_date_str = book["Due Date"]
                due_date_obj = datetime.strptime(due_date_str, "%d-%m-%Y")
                today_date = datetime.today()
                late_days = (today_date - due_date_obj).days  # Calculate late days

                if late_days > 0:
                    fine_amount = (
                        late_days * 50
                    )  # Assuming fine is 50 currency units per late day
                    book["Late Days"] = late_days
                    book["Fine Amount"] = fine_amount
                    print(f"\nLate Return: You are late by {late_days} days!")
                    print(f"Fine Added: RS. {fine_amount}.\n")
                else:
                    book["Late Days"] = 0
                    book["Fine Amount"] = 0
                    print("\nBook returned on time. No fine added.")

                # Update return status and return date
                book["Return Status"] = "Returned"
                book["Return Date"] = datetime.today().strftime("%d-%m-%Y")
                break  # Break the loop once the book is found and processed

        if not book_found:
            print("\nThis book is not issued to this member or already returned!\n")
            input("Press enter to go back...\n")
            return

        # Update book availability
        book_check[0]["Available"] += 1
        book_check[0]["Issued"] -= 1
        if book_check[0]["Available"] > 0:
            book_check[0]["Status"] = "Available"

        # Remove the member from the book's issued-to list
        book_check[0]["Issued-To"] = [
            i for i in book_check[0]["Issued-To"] if i["Member-ID"] != member_id
        ]

        # --- AUTO-DELETE RESERVATION LOGIC ---
                
        # 1. delete member from book's reservation list if this book is reserved by this member
        book_check[0]["Reserved-By"] = [res for res in book_check[0]["Reserved-By"] if res["Member-ID"] != member_id]
                
        # 2. delete this book from member's reserved books list if this book is reserved by this member
        info_check[0]["Reserved Books"] = [res for res in info_check[0]["Reserved Books"] if res["Book-ID"] != book_id]

        # Update JSON files
        Book.update()
        Member.update()

        print(f"\nBook returned successfully. Thank you, {info_check[0]['Name']}!\n")
        input("Press enter to go back...\n")

    def manage_reservations(self):
        while True:
            print("\n--- Manage Reservations ---\n")
            print("1. Reserve a Book")
            print("2. View Book's Waiting List")
            print("3. View Member's Reservations")
            print("4. Cancel a Reservation")
            print("0. Back")
            while True:
                try:
                    choice = int(input("\nEnter your choice: "))
                except ValueError:
                    print("\nResponse must be in digits!\n")
                    continue
                break
            if choice == 0:
                break

            elif choice == 1:
                # --- 1. RESERVE A BOOK ---
                # Member Verification
                while True:
                    member_id = input("Enter Member-ID: ").strip()
                    info_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
                    if len(info_check) == 0:
                        print("\nMember not found!\n")
                        continue
                    if info_check[0]["Status"] == "Blocked" or info_check[0]["Status"] == "Restricted":
                        print("\nMember is blocked/restricted and cannot reserve books!\n")
                        return
                    if len(info_check[0].get("Issued Books", [])) >= 3:
                        print("\nThis member has already issued 3 books! Return a book first to reserve new one.\n")
                        return
                    if len(info_check[0].get("Reserved Books", [])) >= 3:
                        print("\nThis member has already reserved 3 books! Cancel a reservation first to reserve new one.\n")
                        return
                    break

                # Book Verification
                while True:
                    book_id = input("Enter Book-ID: ").strip()
                    book_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(book_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break

                # Check if book is available for issue, if yes then no need to reserve
                if book_check[0]["Status"] == "Available" or book_check[0]["Available"] > 0:
                    print("\nThis book is currently available. No need to reserve!\n")
                    input("Press enter to go back...\n")
                    continue
                    
                # Check if member has already reserved this book, if yes then do not allow to reserve again
                already_reserved = any(res["Member-ID"] == member_id for res in book_check[0]["Reserved-By"])
                if already_reserved:
                    print("\nThis member has already reserved this book!\n")
                    input("Press enter to go back...\n")
                    continue
                
                # Check if member has already issued this book and not returned yet, if yes then do not allow to reserve again
                already_issued = any(
                    (record.get("Book-ID") == book_id and record.get("Return Status") == "Pending") 
                    for record in info_check[0].get("Issued Books", [])
                )
                
                if already_issued:
                    print("\nERROR: This member already has this book issued right now! Return it first.\n")
                    input("Press enter to go back...\n")
                    continue

                # Add reservation record to book's reserved-by list
                date = datetime.today().strftime("%d-%m-%Y")
                book_check[0]["Reserved-By"].append({
                    "Member-ID": member_id,
                    "Name": info_check[0].get("Name", info_check[0].get("Username", "Unknown")), 
                    "Reserve Date": date
                })

                # Add reservation record to member's reserved books list
                info_check[0]["Reserved Books"].append({
                    "Book-ID": book_id,
                    "Title": book_check[0]["Title"],
                    "Reserve Date": date
                })

                # Update JSON files
                Book.update()
                Member.update()
                print(f"\nBook reserved successfully for {info_check[0]['Name']}.\n")
                input("Press enter to go back...\n")

            elif choice == 2:
                # --- 2. VIEW BOOK'S WAITING LIST ---
                while True:
                    book_id = input("Enter Book-ID: ").strip()
                    book_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(book_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break
                # Display waiting list for the book
                # If no reservations, display appropriate message
                res_list = book_check[0]["Reserved-By"]
                if len(res_list) == 0:
                    print("\nNo reservations for this book. The queue is empty.\n")
                else:
                    print(f"\n--- Waiting List for {book_check[0]['Title']} ---")
                    for idx, res in enumerate(res_list, 1):
                        print(f"{idx}. Member-ID: {res['Member-ID']} | Name: {res['Name']} | Date: {res['Reserve Date']}")
                    print("-" * 40 + "\n")
                input("Press enter to go back...\n")

            elif choice == 3:
                # --- 3. VIEW MEMBER'S RESERVATIONS ---
                while True:
                    member_id = input("Enter Member-ID: ").strip()
                    info_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
                    if len(info_check) == 0:
                        print("\nMember not found!\n")
                        continue
                    break

                # Display member's reservations
                # If no reservations, display appropriate message
                res_books = info_check[0]["Reserved Books"]
                if len(res_books) == 0:
                    print("\nThis member has no reservations.\n")
                else:
                    print(f"\n--- Reservations for {info_check[0]['Name']} ---")
                    for idx, res in enumerate(res_books, 1):
                        print(f"{idx}. Book-ID: {res['Book-ID']} | Title: {res['Title']} | Date: {res['Reserve Date']}")
                    print("-" * 40 + "\n")
                input("Press enter to go back...\n")
                    
            elif choice == 4:
                # --- 4. CANCEL A RESERVATION ---
                # Member Verification
                while True:
                    member_id = input("Enter Member-ID: ").strip()
                    info_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
                    if len(info_check) == 0:
                        print("\nMember not found!\n")
                        continue
                    break

                # Book Verification
                while True:
                    book_id = input("Enter Book-ID: ").strip()
                    book_check = [i for i in Book.book_data if i["Book-ID"] == book_id]
                    if len(book_check) == 0:
                        print("\nBook not found!\n")
                        continue
                    break

                # Check if reservation exists, if yes then cancel reservation
                res_exists = any(res["Book-ID"] == book_id for res in info_check[0]["Reserved Books"])
                
                if not res_exists:
                    print("\n❌ No such reservation found for this member and book!\n")
                    continue
                    
                # Remove member from book's reserved-by list 
                # Remove book from member's reserved books list
                book_check[0]["Reserved-By"] = [res for res in book_check[0]["Reserved-By"] if res["Member-ID"] != member_id]
                info_check[0]["Reserved Books"] = [res for res in info_check[0]["Reserved Books"] if res["Book-ID"] != book_id]
                
                Member.update()
                Book.update()
                print(f"\nSUCCESS: Reservation for Book '{book_id}' by Member '{member_id}' has been canceled.\n")
                input("Press enter to go back...\n")

                
            else:
                print("\nInvalid choice! Try again.\n")
