
from datetime import datetime, timedelta
from pathlib import Path
from core.member_base import Member

class MemberViewsMixin:
    def view_issued_books(self):
        # 1. VIP Bouncer: Session Verification
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\nCRITICAL ERROR: No active session found. Please login again.\n")
            return

        user = self.current_user
        
        # Safe Data Fetching (Empty list as fallback to prevent crash)
        issued_books = user.get("Issued Books", [])

        # 2. Empty State Handling (if any book has not been issued yet)
        if len(issued_books) == 0:
            print("\n" + "="*50)
            print(" "*14 + "📚 MY ISSUED BOOKS 📚")
            print("="*50)
            print("\nYou have no issued books in your record history yet.\n")
            input("Press enter to go back...\n")
            return

        # 3. VIP Output Formatting (Card Style display)
        print("\n" + "="*60)
        print(" "*16 + "📚 MY ISSUED BOOKS 📚")
        print("="*60)

        for idx, book in enumerate(issued_books, 1):
            status = book.get("Return Status", "Unknown")
            
            # Dynamic Status Emojis for VIP Look
            status_icon = "⏳ PENDING (Not Returned Yet)" if status == "Pending" else "✅ RETURNED"

            # Book Title Header (Highlighting the main thing)
            print(f"\n[{idx}] 📖 Title: {book.get('Title', 'Unknown')}")
            print("-" * 60)
            
            # Data Alignment formatting (:<16 ensures perfect vertical colons)
            print(f"{'Transaction-ID':<16}: {book.get('Transaction-ID', 'N/A')}")
            print(f"{'Book-ID':<16}: {book.get('Book-ID', 'N/A')}")
            print(f"{'Issue Date':<16}: {book.get('Issue Date', 'N/A')}")
            print(f"{'Due Date':<16}: {book.get('Due Date', 'N/A')}")
            print(f"{'Return Date':<16}: {book.get('Return Date', 'Not Returned')}")
            print(f"{'Status':<16}: {status_icon}")

            # Highlight Fine Details if applicable
            fine_amount = book.get("Fine Amount", 0)
            late_days = book.get("Late Days", 0)
            
            if fine_amount > 0:
                print(f"{'Penalty Alert':<16}: 💸 RS. {fine_amount} (Late by {late_days} days)")
            elif status == "Returned" and fine_amount == 0:
                print(f"{'Penalty Alert':<16}: 🟢 None (Returned on time)")

        print("\n" + "="*60)
        input("\nPress enter to go back to Dashboard...\n")

    def view_reserved_books(self):
        # 1. VIP Bouncer: Session Verification
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\nCRITICAL ERROR: No active session found. Please login again.\n")
            return

        user = self.current_user
        
        # Safe Data Fetching (Empty list as fallback to prevent crash)
        reserved_books = user.get("Reserved Books", [])

        # 2. Empty State Handling (if member has not reserved any book yet)
        if len(reserved_books) == 0:
            print("\n" + "="*50)
            print(" "*12 + "🔖 MY RESERVED BOOKS 🔖")
            print("="*50)
            print("\n⚠️ You have no active reservations at the moment.\n")
            input("Press enter to go back...\n")
            return

        # 3. VIP Output Formatting (Card Style display)
        print("\n" + "="*60)
        print(" "*14 + f"🔖 My RESERVED BOOKS 🔖")
        print("="*60)

        for idx, book in enumerate(reserved_books, 1):
            # Book Title Header (Highlighting the main thing)
            print(f"\n[{idx}] 📖 Title: {book.get('Title', 'Unknown')}")
            print("-" * 60)
            
            # Data Alignment formatting (:<16 ensures perfect vertical colons)
            print(f"{'Book-ID':<16}: {book.get('Book-ID', 'N/A')}")
            print(f"{'Reserve Date':<16}: {book.get('Reserve Date', 'N/A')}")
            
            # Reservation Status Indicator
            print(f"{'Status':<16}: ⏳ RESERVED (Pending Issue)")

        print("\n" + "="*60)
        input("\nPress enter to go back to Dashboard...\n")
