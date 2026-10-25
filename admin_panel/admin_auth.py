from datetime import datetime, timedelta
from pathlib import Path
import re
from core.admin_base import Admin  # VIP Engine Import

class AdminAuthMixin:
    def admin_login(self):
        while True:
            user_name = input("Enter your username: ")
            admin_id = input("Enter your Admin-ID: ")
            password = input("Enter your password: ")
            details = [
                i
                for i in Admin.admin_data
                if i["Username"] == user_name
                and i["Password"] == password
                and i["Admin-ID"] == admin_id
            ]
            if len(details) == 0:
                print("Invalid Credentials! Try Again.")
                continue
            else:
                print(f"Login Successful! Welcome {details[0]["Full Name"]}")
                break
        Admin.update()
        return True

    def changepassword(self):
        print("\n     CHANGE PASSWORD\n", "-" * 37)
        while True:
            admin_id = input("Enter your Admin-ID: ")
            currentpass = input("Enter your current password: ")
            info = [
                i
                for i in Admin.admin_data
                if i["Admin-ID"] == admin_id and i["Password"] == currentpass
            ]
            if len(info) == 0:
                print("Invalid Admin-ID or Current Password! Try Again.")
                continue
            else:

                print(
                    "\n[Password Rule: Min 8 chars, mix of letters, numbers & symbols (i.e. abcd@#123)]\n"
                )
                while True:
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
                    newpass2 = input("Confirm your new password: ")
                    if newpass1 != newpass2:
                        print(
                            "\nPassword doesnot match! please enter same passwords.\n"
                        )
                        continue

                    else:
                        newpass = newpass1
                        if newpass == currentpass:
                            print(
                                "\nNew password can not be same as current password!\n"
                            )
                            continue
                        break
                info[0]["Password"] = newpass
                print("Password changed successsfully!")
                Admin.update()
                input("Press enter to go back: ")
                break

    def updatename(self):
        print("\n     UPDATE NAME\n", "-" * 37)
        while True:
            newname1 = input("Enter your first name: ")
            newname2 = input("Enter your last name: ")
            newname = newname1 + " " + newname2

            if not newname.replace(" ", "").isalpha():
                print("Name can be only in alphabetic characters!")
                continue
            while True:
                admin_id = input("Enter your Admin-ID: ")
                password = input("Enter your password: ")
                info = [
                    i
                    for i in Admin.admin_data
                    if i["Admin-ID"] == admin_id and i["Password"] == password
                ]
                if len(info) == 0:
                    print("Invalid Crendentials! Try Again.\n")
                    continue
                break
            if newname == info[0]["Full Name"]:
                print(f"No changes were made. Your name is already {newname}")
                input("Press enter to go back...")
                break

            info[0]["Full Name"] = newname
            Admin.update()
            print(f"Name successfully updated to {newname}.")
            input("Press enter to go back...")
            break

    def updateemail(self):
        print("\n     UPDATE EMAIL\n", "-" * 37)
        while True:
            newemail = input("Enter your new email (i.e. abc@gmail.com): ").strip()
            email_pattern = (
                r"^(?=[^@][a-zA-Z])[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            )
            if not re.match(email_pattern, newemail):
                print(
                    "Error: Invalid Email Format! Please enter a proper email without weird symbols.\n"
                )
                continue

            check_email = [i for i in Admin.admin_data if i["Email"] == newemail]
            if len(check_email) > 0:
                print("Email already registered! Try different one.\n")
                continue

            print("\n[Security Confirmation]\n")
            while True:
                admin_id = input("Enter your Admin-ID: ")
                password = input("Enter your password: ")
                info = [
                    i
                    for i in Admin.admin_data
                    if i["Admin-ID"] == admin_id and i["Password"] == password
                ]
                if len(info) == 0:
                    print("Invalid Crendentials! Try Again.\n")
                    continue
                break
            info[0]["Email"] = newemail
            Admin.update()
            print(f"Email successfully updated to {newemail}.")
            input("Press enter to go back...")
            break

    def updatephone(self):
        print("\n     UPDATE PHONE NUMBER\n", "-" * 37)
        while True:
            newnumber = input(
                "Enter your new Phone Number (i.e. 03xxxxxxxxx): "
            ).strip()
            number_pattern = r"^(\+?923|03)\d{9}$"
            if not re.match(number_pattern, newnumber):
                print(
                    "Error: Invalid Number Format!\nAccepted formats: [03xxxxxxxxx,923xxxxxxxxx or +923xxxxxxxxx].\n"
                )
                continue

            check_number = [
                i for i in Admin.admin_data if i["Phone Number"] == newnumber
            ]
            if len(check_number) > 0:
                print("Number already registered! Try different one.\n")
                continue
            while True:
                admin_id = input("Enter your Admin-ID: ")
                password = input("Enter your password: ")
                info = [
                    i
                    for i in Admin.admin_data
                    if i["Admin-ID"] == admin_id and i["Password"] == password
                ]
                if len(info) == 0:
                    print("Invalid Crendentials! Try Again.")
                    continue
                break
            info[0]["Phone Number"] = newnumber
            Admin.update()
            print(f"Phone Number successfully updated to {newnumber}.")
            input("Press enter to go back...")
            break

    def updateusername(self):
        print("\n     UPDATE USERNAME\n", "-" * 37)
        while True:
            newusername = input("Enter your new username (i.e. abc_12.3): ").strip()
            username_pattern = r"^(?=.*[a-z])[a-z0-9._]+$"
            if not re.match(username_pattern, newusername):
                print(
                    "Error: Invalid Format!\nUsername must contain at least one lowercase letter,"
                    "0-9"
                    ","
                    "_"
                    ","
                    "."
                    ".\n"
                )
                continue

            check_username = [
                i for i in Admin.admin_data if i["Username"] == newusername
            ]
            if len(check_username) > 0:
                print("Username already exists! Try different one.\n")
                continue
            print("\n[Security Confirmation]\n")
            while True:
                admin_id = input("Enter your Admin-ID: ")
                password = input("Enter your password: ")
                info = [
                    i
                    for i in Admin.admin_data
                    if i["Admin-ID"] == admin_id and i["Password"] == password
                ]
                if len(info) == 0:
                    print("Invalid Crendentials! Try Again.")
                    continue
                break
            info[0]["Username"] = newusername
            Admin.update()
            print(f"Username successfully updated to {newusername}.")
            input("Press enter to go back...")
            break

