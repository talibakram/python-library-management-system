
from datetime import datetime, timedelta
from pathlib import Path
from core.admin_base import Admin
from core.member_base import Member

class AdminFinancesMixin:
    def view_unpaid_fines(self):
        print("\n" + "="*60)
        print(" "*20 + "VIEW UNPAID FINES")
        print("="*60 + "\n")
        
        found_defaulters = False
        print(f"{'Member-ID':<18} | {'Name':<20} | {'Unpaid Amount'}")
        print("-" * 60)

        # Scan through all members to find those with unpaid fines
        for member in Member.member_data:
            total_fine = member.get("Total Fine", 0)
            paid_fine = member.get("Paid Fine", 0)
            
            # Calculate unpaid amount
            unpaid_amount = total_fine - paid_fine

            if unpaid_amount > 0:
                found_defaulters = True
                name = member.get("Name", member.get("Username", "Unknown"))
                print(f"{member['Member-ID']:<18} | {name:<20} | Rs. {unpaid_amount}")

        if not found_defaulters:
            print(f"{'':<10} ✅ All clear! No members have any pending fines.")

        print("-" * 60)
        input("\nPress enter to go back...\n")

    def record_fine_payment(self):
        print("\n" + "="*60)
        print(" "*20 + "RECORD FINE PAYMENT")
        print("="*60 + "\n")

        while True:
            member_id = input("Enter Member-ID: ").strip()
            member_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
            if len(member_check) == 0:
                print("\nMember not found!\n")
                continue
            break
        # Retrieve the member's information
        member = member_check[0]
        total_fine = member.get("Total Fine", 0)
        paid_fine = member.get("Paid Fine", 0)
        unpaid_amount = total_fine - paid_fine

        if unpaid_amount <= 0:
            print(f"\n✅ Member '{member['Name']}' has no pending fines.\n")
            input("Press enter to go back...\n")
            return

        print(f"\nMember '{member['Name']}' has an unpaid fine of Rs. {unpaid_amount}.\n")

        # Get payment amount from user
        while True:
            try:
                payment_amount = float(input("Enter payment amount: Rs. ").strip())
            except ValueError:
                print("\nInvalid input! Please enter a valid number.\n")
                continue
            if payment_amount <= 0:
                print("\nPayment amount must be greater than zero!\n")
                continue
            if payment_amount > unpaid_amount:
                print(f"\nPayment exceeds unpaid amount! Max allowed: Rs. {unpaid_amount}\n")
                continue
            break

        # Update the paid fine amount
        member["Paid Fine"] = paid_fine + payment_amount
        date = datetime.today().strftime("%d-%m-%Y")
        
        # Maintain fine payment history for the member
        if "Fine History" not in member:
            member["Fine History"] = []
            
        member["Fine History"].append({
            "Paid Amount": payment_amount,
            "Date": date
        })
        
        # 5. Save and Success Message
        Member.update()
        
        remaining = unpaid_amount - payment_amount
        print(f"\nSUCCESS: Rs. {payment_amount} received from {member.get('Name', 'Unknown')}.")
        print(f"ℹRemaining Fine Balance: Rs. {remaining}\n")
        
        input("Press enter to go back...\n")
