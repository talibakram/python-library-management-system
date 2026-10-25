
from datetime import datetime, timedelta
from pathlib import Path
import re
from core.member_base import Member  # VIP Engine Import

class MemberProfileMixin:
    def view_profile(self):
        # Check if the user is logged in
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\nCRITICAL ERROR: No active session found. Please login again.\n")
            return
        
        user = self.current_user

        print("\n" + "="*55)
        print(" "*18 + "👤 MY PROFILE DETAILS 👤")
        print("="*55 + "\n")

        # 2. Display Details (Safe Data Fetching with .get() to prevent KeyError)
        print(f"{'Full Name':<15}: {user.get('Name', 'N/A')}")
        print(f"{'Member-ID':<15}: {user.get('Member-ID', 'N/A')}")
        print(f"{'Username':<15}: {user.get('Username', 'N/A')}")
        print(f"{'Email':<15}: {user.get('Email', 'N/A')}")
        print(f"{'Phone No':<15}: {user.get('Phone Number', 'N/A')}")
        print(f"{'CNIC No':<15}: {user.get('CNIC No', 'N/A')}")
        print(f"{'University':<15}: {user.get('University', 'N/A')}")
        print(f"{'Department':<15}: {user.get('Department', 'N/A')}")
        print(f"{'Roll No':<15}: {user.get('Roll No', 'N/A')}")

        # 3. Account Status Details
        print("\n--- Account Status ---")
        status = user.get('Status', 'Unknown').title()

        # VIP Trick: Dynamic Emojis based on active/blocked status
        status_icon = "🟢" if status == "Active" else "🔴"

        print(f"Status        : {status_icon} {status}")
        print(f"Joined On     : {user.get('Registration Date', 'N/A')}")
        
        print("\n" + "="*55)
        input("\nPress enter to go back...\n")

    def edit_details(self):
        # Check if the user is logged in
        if not hasattr(self, 'current_user') or not self.current_user:
            print("\n❌ CRITICAL ERROR: No active session found. Please login again.\n")
            return
        user = self.current_user

        while True:
            print("\n" + "="*50)
            print(" "*16 + "⚙️ EDIT MY PROFILE ⚙️")
            print("="*50)
            print("What do you want to update?")
            print("1. Edit Name")
            print("2. Edit Phone Number")
            print("3. Edit Email Address")
            print("4. Change Username")
            print("5. Change Password")
            print("0. Back")
            print("="*50)
            while True:
                try:
                    choice = int(input("\nWhat would you like to update? (0-5): "))
                except ValueError:
                    print("\nInvalid input! Please enter a number between 0 and 5.\n")
                    continue
                break
            if choice == 0:
                break
            elif choice == 1:
                while True:
                    print("Enter new name below:")
                    newname1 = input("First Name: ").strip().title()
                    newname2 = input("Last Name: ").strip().title()
                    newname = newname1 + " " + newname2
                    # VIP Trick: Allowing spaces in name but ensuring only alphabetic characters
                    if not newname.replace(" ", "").isalpha():
                        print("\nName can be only in alphabetic characters!\n")
                        continue
                    user["Name"] = newname
                    Member.update()
                    print(f"\nName successfully updated to {newname}.")
                    input("\nPress enter to go back...\n")
                    break

            elif choice == 2:
                print("Update phone number:")
                while True:
                    newnumber = input("New Phone Number (i.e. 03xxxxxxxxx): ").strip()
                    # VIP Trick: More robust phone number validation pattern that allows optional country code and ensures correct length and format
                    number_pattern = r"^(\+?923|03)\d{9}$"
                    if not re.match(number_pattern, newnumber):
                        print(
                            "\nError: Invalid Number!\nAccepted formats: [03xxxxxxxxx,923xxxxxxxxx or +923xxxxxxxxx].\n"
                        )
                        continue
                    # VIP Trick: Check for number uniqueness across all members
                    check_number = [
                        i for i in Member.member_data if i["Phone Number"] == newnumber
                    ]
                    if len(check_number) > 0:
                        print("\nNumber already registered! Try different one.\n")
                        continue
                    user["Phone Number"] = newnumber
                    Member.update()
                    print(f"\nPhone Number successfully updated to {newnumber}.\n")
                    input("Press enter to go back...\n")
                    break

            elif choice == 3:
                print("Update email address:")
                while True:
                    newemail = input("New Email (i.e. abc@gmail.com): ").strip()
                    # VIP Trick: More robust email validation pattern that checks for proper structure and prevents common mistakes
                    email_pattern = r"^(?=[^@][a-zA-Z])[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                    if not re.match(email_pattern, newemail):
                        print("\nError: Invalid Email! Please enter a proper email.\n")
                        continue
                    # VIP Trick: Check for email uniqueness across all members
                    check_email = [
                        i for i in Member.member_data if i["Email"] == newemail
                    ]
                    if len(check_email) > 0:
                        print("\nEmail already registered! Try different one.\n")
                        continue
                    user["Email"] = newemail
                    Member.update()
                    print(f"\nEmail successfully updated to {newemail}.\n")
                    input("Press enter to go back...\n")
                    break

            elif choice == 4:
                print("Update member's username:")
                while True:
                    username = input("New Username: ").strip()
                    # VIP Trick: More robust username validation pattern that ensures at least one lowercase letter and allows only specific characters
                    username_pattern = r"^(?=.*[a-z])[a-z0-9._]+$"
                    if not re.match(username_pattern, username):
                        print(
                            "Error: Username not available!\nUsername must contain at least one lowercase letter,"
                            "0-9"
                            ","
                            "_"
                            ","
                            "."
                            ".\n"
                        )
                        continue
                    # VIP Trick: Check for username uniqueness across all members
                    check_username = [
                        i for i in Member.member_data if i["Username"] == username
                    ]
                    if len(check_username) > 0:
                        print("\nUsername already exists! Try different one.\n")
                        continue
                    user["Username"] = username
                    Member.update()
                    print(f"\nUsername successfully updated to {username}.\n")
                    input("Press enter to go back...\n")
                    break

            elif choice == 5:
                while True:
                    currentpass = input("Enter your current password: ")
                    # VIP Trick: Directly comparing current password with the logged-in user's password to ensure security and prevent unauthorized changes
                    if currentpass != user["Password"]:
                        print("\nCurrent password is incorrect! Try again.\n")
                        continue
                    break
                while True:
                    print(
                            "\n[Password Rule: Min 8 chars, mix of letters, numbers & symbols (i.e. abcd@#123)]\n"
                        )
                        
                    newpass1 = input("Enter your new password: ")
                    if len(newpass1) < 8:
                        print(
                                    "\nMinimun 8 characters length of password is required!\n"
                                )
                        continue
                    has_letter = any(char.isalpha() for char in newpass1)
                    has_number = any(char.isdigit() for char in newpass1)
                    has_symbol = any(not char.isalnum() for char in newpass1)
                    if not (has_letter and has_number and has_symbol):
                        print(
                                    "\nError! Password should be mix of letters, numbers & symbols.\n"
                                )
                        continue
                    
                    while True:
                        newpass2 = input("Confirm your new password: ")
                        if newpass1 != newpass2:
                            print(
                                    "\nPassword doesnot match! please enter same passwords.\n"
                                )
                            continue
                        break

                    newpass = newpass1
                    if newpass == currentpass:
                        print(
                                        "\nNew password can not be same as current password!\n"
                                    )
                        continue
                    break
                user["Password"] = newpass
                print("Password changed successsfully!")
                Member.update()
                input("Press enter to go back: ")
                break
