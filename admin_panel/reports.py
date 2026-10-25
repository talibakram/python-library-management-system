
from datetime import datetime, timedelta
from pathlib import Path

from core.admin_base import Admin
from core.member_base import Member
from core.book_model import Book

class ReportsSystemMixin:
    def view_overdue_books(self):
        print("\n" + "="*95)
        print(" "*35 + "🚨 OVERDUE BOOKS REPORT 🚨")
        print("="*95 + "\n")

        # Header for the report
        print(f"{'Member-ID':<16} | {'Name':<18} | {'Book-ID':<18} | {'Title':<20} | {'Due Date':<10} | {'Late Days'}")
        print("-" * 95)
        
        found_overdue = False

        # Get today's date for comparison
        today_date = datetime.today()

        # Scan through all members and their borrowed books to find overdue items   
        for member in Member.member_data:
            # Get list of issued books for the member
            issued_books = member.get("Issued Books", [])
            # Inner loop to check each issued book for overdue status
            for record in issued_books:
                if record.get("Return Status") == "Pending":
                    due_date_str = record.get("Due Date")
                    
                    try:
                        due_date_obj = datetime.strptime(due_date_str, "%d-%m-%Y")
                        late_days = (today_date - due_date_obj).days
                        if late_days > 0:
                            found_overdue = True
                            name = member.get("Name", member.get("Username", "Unknown"))
                            title = record.get("Title", "Unknown")
                            if len(title) > 18:
                                title = title[:15] + "..."
                            member_id = member.get("Member-ID", "Unknown")
                            print(f"{member_id:<16} | {name:<18} | {record.get('Book-ID', 'Unknown'):<18} | {title:<20} | {due_date_str:<10} | {late_days} Days")
                    except ValueError:
                        continue
        if not found_overdue:
            print(f"{'':<25} Good News! No books are currently overdue.")
            
        print("-" * 95)
        input("\nPress enter to go back...\n")

    def view_library_dashboard(self):
        today_date = datetime.today()

        # ==========================================
        # 1. DATA COLLECTION & CALCULATION ENGINE
        # ==========================================

        # --- Inventory Variables ---
        total_book_titles = len(Book.book_data)
        total_available = 0
        total_issued = 0
        total_reservations = 0

        # Inventory Calculation Loop
        for book in Book.book_data:
            total_available += book.get("Available", 0)
            total_issued += book.get("Issued", 0)
            total_reservations += len(book.get("Reserved-By", []))

        # --- Membership & Financial Variables ---
        total_members = len(Member.member_data)
        active_members = 0
        blocked_members = 0
        
        total_fine_collected = 0
        total_pending_fine = 0
        total_overdue_books = 0

        # Membership, Financial & Overdue Calculation Loop
        for member in Member.member_data:
            status = member.get("Status", "Unknown").title()
            if status == "Active":
                active_members += 1
            elif status in ["Blocked", "Inactive", "Restricted"]:
                blocked_members += 1
                
            total_fine = member.get("Total Fine", 0)
            paid_fine = member.get("Paid Fine", 0)

            total_fine_collected += paid_fine
            total_pending_fine += (total_fine - paid_fine)

            for record in member.get("Issued Books", []):
                if record.get("Return Status") == "Pending":
                    due_date_str = record.get("Due Date", "")
                    try:
                        due_date_obj = datetime.strptime(due_date_str, "%d-%m-%Y")
                        if (today_date - due_date_obj).days > 0:
                            total_overdue_books += 1
                    except ValueError:
                        pass

        # ==========================================
        # 2. UI / DISPLAY ENGINE
        # ==========================================
        print("\n" + "="*75)
        print(" "*22 + "📊 LIBRARY CONTROL DASHBOARD 📊")
        print("="*75 + "\n")
        
        # Left Column: Inventory, Right Column: Membership
        print(f"{'[📚 INVENTORY]':<38} {'[👥 MEMBERSHIP]'}")
        print(f"{'Total Titles:':<16} {total_book_titles:<21} {'Total Members:':<16} {total_members}")
        print(f"{'Available:':<16} {total_available:<21} {'Active:':<16} {active_members}")
        print(f"{'Issued:':<16} {total_issued:<21} {'Blocked:':<16} {blocked_members}")
        print()
        
        # Left Column: Financials, Right Column: Alerts
        print(f"{'[💸 FINANCIALS]':<38} {'[🚨 ALERTS]'}")
        print(f"{'Fine Collected:':<16} Rs. {total_fine_collected:<17} {'Overdue Books:':<20} {total_overdue_books}")
        print(f"{'Pending Fine:':<16} Rs. {total_pending_fine:<17} {'Active Reserves:':<20} {total_reservations}")
        
        print("\n" + "="*75)
        input("\nPress enter to go back...\n")

    def view_reports(self):
        while True:
            # VIP Reports Sub-Menu
            print("\n" + "="*50)
            print(" "*14 + "SYSTEM REPORTS MENU")
            print("="*50)
            print("1. Top Popular Books (Trending)")
            print("2. Blocked / Restricted Members")
            print("3. Out-of-Stock Books")
            print("0. Back")
            print("="*50)
            
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
                # --- 1. TOP POPULAR BOOKS (TRENDING) ---
                print("\n" + "-"*75)
                print(" "*22 + "TOP 5 POPULAR BOOKS")
                print("-"*75)
                print(f"{'Rank':<5} | {'Book-ID':<18} | {'Title':<28} | {'Total Issued'}")
                print("-"*75)
                
                # Sort books by the number of times they've been issued (in descending order)
                sorted_books = sorted(Book.book_data, key=lambda x: x.get("Issued", 0), reverse=True)
                
                # Get top 5 books from the sorted list
                top_5 = sorted_books[:5]
                
                # Display the top 5 books in a formatted manner
                for idx, book in enumerate(top_5, 1):
                    title = book.get("Title", "Unknown")
                    # Truncate title if it's too long for display
                    if len(title) > 25:
                        title = title[:22] + "..."
                        
                    print(f"{idx:<5} | {book.get('Book-ID', 'Unknown'):<18} | {title:<28} | {book.get('Issued', 0)} times")
                    
                print("-"*75)
                input("\nPress enter to go back...\n")
                
            elif choice == 2:
                # --- 2. BLOCKED & RESTRICTED MEMBERS ---
                print("\n" + "-"*85)
                print(" "*25 + "BLOCKED & RESTRICTED MEMBERS")
                print("-"*85)
                print(f"{'Member-ID':<18} | {'Name':<20} | {'Status':<12} | {'Unpaid Fine'}")
                print("-"*85)
                
                found_blocked = False
                # Scan through all members to find those with status "Blocked" or "Restricted"
                for member in Member.member_data:
                    status = member.get("Status", "Unknown").title()
                    
                    if status in ["Blocked", "Restricted"]:
                        found_blocked = True
                        name = member.get("Name", member.get("Username", "Unknown"))
                        
                        # Calculate unpaid fine amount for the member
                        unpaid = member.get("Total Fine", 0) - member.get("Paid Fine", 0)
                        
                        print(f"{member.get('Member-ID', 'Unknown'):<18} | {name:<20} | {status:<10} | Rs. {unpaid}")
                        
                if not found_blocked:
                    print(f"{'':<20} All clear! No blocked or restricted members found.")
                    
                print("-"*85)
                input("\nPress enter to go back...\n")
                
            elif choice == 3:
                # --- 3. OUT-OF-STOCK BOOKS ---
                print("\n" + "-"*80)
                print(" "*25 + "OUT-OF-STOCK BOOKS")
                print("-"*80)
                print(f"{'Book-ID':<18} | {'Title':<25} | {'Category':<15} | {'Total Copies'}")
                print("-"*80)
                
                found_oos = False
                # Scan through all books to find those with availability 0 or status "Out Of Stock"
                for book in Book.book_data:
                    if book.get("Available", 0) == 0:
                        found_oos = True
                        
                        title = book.get("Title", "Unknown")
                        if len(title) > 23:
                            title = title[:20] + "..."
                        
                        # Truncate category if it's too long for display
                        category = book.get("Category", "Unknown")
                        if len(category) > 13:
                            category = category[:10] + "..."
                            
                        print(f"{book.get('Book-ID', 'Unknown'):<18} | {title:<25} | {category:<15} | 🛑 {book.get('Total Copies', 0)}")
                        
                if not found_oos:
                    print(f"{'':<20} Stock is healthy! No books are completely out of stock.")
                    
                print("-"*80)
                input("\nPress enter to go back...\n")
                
            else:
                print("\nInvalid choice! Please select an option between 0 and 3.\n")
                
    def view_activity_logs(self):
        while True:
            print("\n" + "="*50)
            print(" "*14 + "SYSTEM ACTIVITY LOGS")
            print("="*50)
            print("1. Recent Issue & Return Logs")
            print("2. Fine Payment History")
            print("0. Back")
            print("="*50)
            
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
                # --- 1. RECENT ISSUE & RETURN LOGS ---
                print("\n" + "-"*85)
                print(" "*25 + "RECENT TRANSACTIONS LOG")
                print("-"*85)
                print(f"{'Date':<12} | {'Member-ID':<18} | {'Action':<10} | {'Book-ID':<18} | {'TRX-ID'}")
                print("-"*85)
                
                all_transactions = []
                
                # Collect Transaction Data 
                for member in Member.member_data:
                    member_id = member.get("Member-ID", "Unknown")
                    for record in member.get("Issued Books", []):
                        
                        # 1. Collect Issue Record if the book has been issued
                        issue_date = record.get("Issue Date")
                        if issue_date:
                            all_transactions.append({
                                "Date_Str": issue_date,
                                "Member": member_id,
                                "Action": "ISSUED",
                                "Book": record.get("Book-ID", "Unknown"),
                                "TRX": record.get("Transaction-ID", "Unknown")
                            })
                            
                        # 2. Collect Return Record (if the book has been returned)
                        if record.get("Return Status") == "Returned":
                            return_date = record.get("Return Date")
                            if return_date:
                                all_transactions.append({
                                    "Date_Str": return_date,
                                    "Member": member_id,
                                    "Action": "RETURNED",
                                    "Book": record.get("Book-ID", "Unknown"),
                                    "TRX": record.get("Transaction-ID", "Unknown")
                                })
                
                # Sort all transactions by date in descending order (most recent first)
                try:
                    all_transactions.sort(key=lambda x: datetime.strptime(x["Date_Str"], "%d-%m-%Y"), reverse=True)
                except ValueError:
                    pass 
                
                # Display the top 15 recent transactions 
                if not all_transactions:
                    print(f"{'':<20} No recent transactions found in the system.")
                else:
                    for log in all_transactions[:15]:
                        action_icon = "🟢" if log["Action"] == "ISSUED" else "🔵"
                        print(f"{log['Date_Str']:<12} | {log['Member']:<18} | {action_icon} {log['Action']:<8} | {log['Book']:<18} | {log['TRX']}")
                
                print("-"*85)
                input("\nPress enter to go back...\n")
                
            elif choice == 2:
                # --- 2. FINE PAYMENT HISTORY ---
                print("\n" + "-"*65)
                print(" "*20 + "💸 RECENT FINE PAYMENTS 💸")
                print("-"*65)
                print(f"{'Date':<12} | {'Member-ID':<18} | {'Name':<18} | {'Paid Amount'}")
                print("-"*65)
                
                all_payments = []
                
                for member in Member.member_data:
                    member_id = member.get("Member-ID", "Unknown")
                    name = member.get("Name", member.get("Username", "Unknown"))
                    
                    # Collect Fine Payment Records from the member's fine history
                    for receipt in member.get("Fine History", []):
                        date_str = receipt.get("Date")
                        amount = receipt.get("Paid Amount", receipt.get("Amount", 0)) # Agar key Amount hy ya Paid Amount
                        
                        if date_str and amount > 0:
                            all_payments.append({
                                "Date_Str": date_str,
                                "Member": member_id,
                                "Name": name,
                                "Amount": amount
                            })
                            
                # Sort all fine payments by date in descending order (most recent first)
                try:
                    all_payments.sort(key=lambda x: datetime.strptime(x["Date_Str"], "%d-%m-%Y"), reverse=True)
                except ValueError:
                    pass
                
                if not all_payments:
                    print(f"{'':<15} No fine payment history found.")
                else:
                    # Top 15 payments
                    for pay in all_payments[:15]:
                        name_str = pay["Name"]
                        if len(name_str) > 15:
                            name_str = name_str[:12] + "..."
                            
                        print(f"{pay['Date_Str']:<12} | {pay['Member']:<18} | {name_str:<18} | 💰 Rs. {pay['Amount']}")
                
                print("-"*65)
                input("\nPress enter to go back...\n")
                
            else:
                print("\nInvalid choice! Please select an option between 0 and 2.\n")
