
from datetime import datetime, timedelta
from pathlib import Path
from core.member_base import Member

class MemberFinancesMixin:
    def pay_fine(self):
        import random
        from datetime import datetime

        # 1. VIP Bouncer: Session Verification
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\nCRITICAL ERROR: No active session found. Please login again.\n")
            return

        user = self.current_user

        # Fetching current fine details safely
        total_fine = user.get("Total Fine", 0)
        paid_fine = user.get("Paid Fine", 0)

        # 2. Empty Fine State (Agar account pehle se clear hy)
        if total_fine <= 0:
            print("\n" + "="*50)
            print(" "*18 + "💸 PAY FINE 💸")
            print("="*50)
            print("\n🎉 Awesome! You have no pending fines. Your account is totally clear!\n")
            input("Press enter to go back...\n")
            return

        while True:
            print("\n" + "="*50)
            print(" "*18 + "💸 PAY FINE 💸")
            print("="*50)
            print(f"Total Pending Fine : RS. {total_fine}")
            print(f"Total Paid So Far  : RS. {paid_fine}")
            print("-" * 50)
            print("Enter the amount you want to pay (or '0' to cancel).")
            
            # Crash-Proof Input Validation
            try:
                payment = int(input("\nEnter amount: RS. "))
            except ValueError:
                print("\nInvalid input! Please enter digits only.\n")
                continue

            if payment == 0:
                print("\nTransaction cancelled. Returning to Dashboard...\n")
                break
            
            # Banking Security: Prevent Negative Values
            if payment < 0:
                print("\nAmount cannot be negative!\n")
                continue

            # Banking Security: Prevent Over-Paying
            if payment > total_fine:
                print(f"\nYou only owe RS. {total_fine}. You cannot pay more than your pending fine!\n")
                continue

            # --- VIP PAYMENT PROCESSING ---
            
            # 1. Update Finances
            user["Total Fine"] -= payment
            user["Paid Fine"] = user.get("Paid Fine", 0) + payment

            # 2. Generate Receipt Details
            date_str = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
            receipt_id = f"REC.{random.randint(100000, 999999)}"

            receipt = {
                "Receipt-ID": receipt_id,
                "Date": date_str,
                "Amount Paid": payment,
                "Remaining Fine": user["Total Fine"]
            }

            # 3. Add to Fine History safely
            user.setdefault("Fine History", []).append(receipt)

            # 4. Database Save
            Member.update()

            # 5. Print VIP Digital Receipt
            print("\n" + "*"*55)
            print(" "*18 + "🧾 PAYMENT RECEIPT 🧾")
            print("*"*55)
            print(f"{'Receipt-ID':<16}: {receipt_id}")
            print(f"{'Date & Time':<16}: {date_str}")
            print(f"{'Member Name':<16}: {user.get('Name')}")
            print(f"{'Amount Paid':<16}: 💸 RS. {payment}")
            print(f"{'Remaining Dues':<16}: RS. {user['Total Fine']}")
            print("*"*55)
            print("\nPayment successful! Thank you for clearing your dues.\n")
            
            input("Press enter to go back...\n")
            break

    def view_fine_history(self):
        # 1. VIP Bouncer: Session Verification
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\nCRITICAL ERROR: No active session found. Please login again.\n")
            return

        user = self.current_user
        
        # Safe Data Fetching (Empty list as fallback to prevent crash)
        fine_history = user.get("Fine History", [])

        # 2. Empty State Handling (Agar koi purani payment history nahi hy)
        if len(fine_history) == 0:
            print("\n" + "="*50)
            print(" "*14 + "🧾 FINE PAYMENT HISTORY 🧾")
            print("="*50)
            print("\n🟢 No fine history found! Your account has no past penalties.\n")
            input("Press enter to go back...\n")
            return

        # 3. VIP Output Header & Overall Fine Summary
        print("\n" + "="*60)
        print(" "*15 + f"🧾 FINE HISTORY FOR {user.get('Name', 'USER').upper()} 🧾")
        print("="*60)
        # Summary metrics
        print(f"{'Current Pending Fine':<24}: RS. {user.get('Total Fine', 0)}")
        print(f"{'Total Fine Paid':<24}: RS. {user.get('Paid Fine', 0)}")
        print("="*60)

        # 4. Loop Through Receipts (Using enumerate for perfect numbering)
        for idx, receipt in enumerate(fine_history, 1):
            print(f"\n[{idx}] 🧾 Receipt Details")
            print("-" * 60)
            
            # Data Alignment formatting (:<18 ensures perfect vertical colons)
            print(f"{'Receipt-ID':<18}: {receipt.get('Receipt-ID', 'N/A')}")
            print(f"{'Payment Date/Time':<18}: {receipt.get('Date', 'N/A')}")
            print(f"{'Amount Paid':<18}: 💸 RS. {receipt.get('Amount Paid', 0)}")
            print(f"{'Remaining Dues':<18}: RS. {receipt.get('Remaining Fine', 0)}")
            print("-" * 60)

        print("\n" + "="*60)
        input("\nPress enter to go back to Dashboard...\n")
