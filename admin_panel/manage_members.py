
from datetime import datetime, timedelta
from pathlib import Path

import re
from datetime import datetime
from core.admin_base import Admin
from core.member_base import Member 

class ManageMembersMixin:
    def addmember(self):
        print("\n       MEMBER REGISTRATION\n", "-" * 37)
        while True:
            print("Enter Member Details:\n")
            name1 = input("First name: ").strip().title()
            name2 = input("Last name: ").strip().title()
            name = name1 + " " + name2
            if not name.replace(" ", "").isalpha():
                print("\nName can be only in alphabetic characters!\n")
                continue
            while True:
                try:
                    age = int(input("Age: "))
                except ValueError:
                    print("\nAge must be in digits!\n")
                    continue
                if age < 16:
                    print("\nMember's age must be 16 0r 16+!\n")
                    continue
                break
            while True:
                rollno = input("Roll Number: ").strip()
                roll_pattern = r"^[a-zA-Z0-9_.-]{1,15}$"
                if not re.match(roll_pattern, rollno):
                    print("\nInvalid roll number! please enter valid roll number.\n")
                    continue
                check_roll = [i for i in Member.member_data if i["Roll No"] == rollno]
                if len(check_roll) > 0:
                    print("\nMember with this roll number already exists!\n")
                    continue
                break

            while True:
                cnic = input("13 digit CNIC number: ").strip()
                cnic_pattern = r"^[1-8]\d{4}-?\d{7}-?\d{1}$"
                if not re.match(cnic_pattern, cnic):
                    print("\nInvalid CNIC number! Please valid CNIC number.\n")
                    continue
                if "-" not in cnic:
                    formatedcnic = f"{cnic[:5]}-{cnic[5:12]}-{cnic[12:]}"
                    cnic = formatedcnic
                check_cnic = [i for i in Member.member_data if i["CNIC No"] == cnic]
                if len(check_cnic) > 0:
                    print("\nMember with this cnic number already exists!\n")
                    continue
                break
            while True:
                dept = input("Department: ").strip().title()
                dept_pattern = r"^[a-zA-Z\s.&-]+$"
                if not re.match(dept_pattern, dept):
                    print("\nPlease enter a correct department name!\n")
                    continue
                break
            while True:
                university = input("University name: ").strip().title()
                if not re.match(dept_pattern, university):
                    print("\nPlease enter correct university name!\n")
                    continue
                break
            while True:
                email = input("Email adress: ").strip()
                email_pattern = (
                    r"^(?=[^@][a-zA-Z])[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                )
                if not re.match(email_pattern, email):
                    print("\nError: Invalid Email! Please enter a proper email.\n")
                    continue

                check_email = [i for i in Member.member_data if i["Email"] == email]
                if len(check_email) > 0:
                    print("\nEmail already registered! Try different one.\n")
                    continue
                break

            while True:
                phonenumber = input("Phone number: ").strip()
                number_pattern = r"^(\+?923|03)\d{9}$"
                if not re.match(number_pattern, phonenumber):
                    print(
                        "\nError: Invalid Number!\nAccepted formats: [03xxxxxxxxx,923xxxxxxxxx or +923xxxxxxxxx].\n"
                    )
                    continue

                check_number = [
                    i for i in Member.member_data if i["Phone Number"] == phonenumber
                ]
                if len(check_number) > 0:
                    print("\nNumber already registered! Try different one.\n")
                    continue
                break

            member_info = {
                "Name": name,
                "Age": age,
                "Roll No": rollno,
                "CNIC No": cnic,
                "Department": dept,
                "University": university,
                "Email": email,
                "Phone Number": phonenumber,
                "Member-ID": Member.uniqueid(),
                "Username": Member.usernamegenerate(name),
                "Password": Member.autopassword(),
                "Registration Date": datetime.today().strftime("%d-%m-%Y"),
                "Status": "Active",
                "Issued Books": [],
                "Paid Fine": 0,
                "Total Fine": 0,
                "Fine History": [],
            }
            break
        Member.member_data.append(member_info)
        Member.update()
        print("\n---Member registered successfully---\n")
        print("Here's your account details\n")

        print(
            f"Please remember your important details:\nUsername : {member_info['Username']}\nMember-ID : {member_info['Member-ID']}\nPassword : {member_info['Password']}"
        )
        print("\nThankyou for registering with us.")
        input("\nPress enter to go back...")

    def view_memberdetails(self):
        while True:
            member_id = input("\nEnter member's Member-ID: ")
            id_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
            if len(id_check) == 0:
                print("\nMember not not found! Please enter correct Member-ID.\n")
                continue
            break
        print("\nHere's member's details:")
        for i in id_check[0]:
            print(f"{i} : {id_check[0][i]}")
        input("\nPress enter to go back...")

    def update_member_details(self):
        while True:
            member_id = input("Enter member's Member-ID: ")
            id_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
            if len(id_check) == 0:
                print("User not found!")
                continue
            break
        member_dict = id_check[0]
        while True:
            print("\nUpdate member details below:\n")
            print("1. Name")
            print("2. Age")
            print("3. Username")
            print("4. Email")
            print("5. Phone Number")
            print("6. Password")
            print("7. CNIC No.")
            print("8. Roll No.")
            print("9. Department")
            print("10. University")
            print("11. Status")
            print("0. Back\n")

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
                    print("Update member's name below:")
                    newname1 = input("First Name: ").strip().title()
                    newname2 = input("Last Name: ").strip().title()
                    newname = newname1 + " " + newname2
                    if not newname.replace(" ", "").isalpha():
                        print("\nName can be only in alphabetic characters!\n")
                        continue
                    member_dict["Name"] = newname
                    Member.update()
                    print(f"\nName successfully updated to {newname}.")
                    input("\nPress enter to go back...\n")
                    break
            elif choice == 2:
                print("Update member's age:")
                while True:
                    try:
                        age = int(input("New Age (must be 16 or 16+): "))
                    except ValueError:
                        print("\nAge must be in digits!\n")
                        continue
                    if age < 16:
                        print("\nAge must be 16 or 16+!\n")
                        continue
                    member_dict["Age"] = age
                    Member.update()
                    print(f"\nAge successfully updated to {age}\n")
                    input("Press enter to go back...")
                    break
            elif choice == 3:
                print("Update member's username:")
                while True:
                    username = input("New Username: ").strip()
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

                    check_username = [
                        i for i in Member.member_data if i["Username"] == username
                    ]
                    if len(check_username) > 0:
                        print("\nUsername already exists! Try different one.\n")
                        continue
                    member_dict["Username"] = username
                    Member.update()
                    print(f"\nUsername successfully updated to {username}.\n")
                    input("Press enter to go back...\n")
                    break
            elif choice == 4:
                print("Update member's email:")
                while True:
                    newemail = input("New Email (i.e. abc@gmail.com): ").strip()
                    email_pattern = r"^(?=[^@][a-zA-Z])[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                    if not re.match(email_pattern, newemail):
                        print("\nError: Invalid Email! Please enter a proper email.\n")
                        continue

                    check_email = [
                        i for i in Member.member_data if i["Email"] == newemail
                    ]
                    if len(check_email) > 0:
                        print("\nEmail already registered! Try different one.\n")
                        continue
                    member_dict["Email"] = newemail
                    Member.update()
                    print(f"\nEmail successfully updated to {newemail}.\n")
                    input("Press enter to go back...\n")
                    break

            elif choice == 5:
                print("Update member's phone number:")
                while True:
                    newnumber = input("New Phone Number (i.e. 03xxxxxxxxx): ").strip()
                    number_pattern = r"^(\+?923|03)\d{9}$"
                    if not re.match(number_pattern, newnumber):
                        print(
                            "\nError: Invalid Number!\nAccepted formats: [03xxxxxxxxx,923xxxxxxxxx or +923xxxxxxxxx].\n"
                        )
                        continue

                    check_number = [
                        i for i in Member.member_data if i["Phone Number"] == newnumber
                    ]
                    if len(check_number) > 0:
                        print("\nNumber already registered! Try different one.\n")
                        continue
                    member_dict["Phone Number"] = newnumber
                    Member.update()
                    print(f"\nPhone Number successfully updated to {newnumber}.\n")
                    input("Press enter to go back...\n")
                    break
            elif choice == 6:
                print("Update member's password:")
                while True:
                    newpass1 = input("New Password: ").strip()
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
                    if newpass == member_dict["Password"]:
                        print("\nNew password can not be same as current password!\n")
                        continue
                    member_dict["Password"] = newpass
                    print(f"\nPassword updated successsfully to {newpass}.\n")
                    Member.update()
                    input("Press enter to go back...\n")
                    break
            elif choice == 7:
                print("Update member's CNIC No.:")
                while True:
                    cnic = input("13 digit CNIC number: ").strip()
                    cnic_pattern = r"^[1-8]\d{4}-?\d{7}-?\d{1}$"
                    if not re.match(cnic_pattern, cnic):
                        print("\nInvalid CNIC number! Please valid CNIC number.\n")
                        continue
                    if "-" not in cnic:
                        formatedcnic = f"{cnic[:5]}-{cnic[5:12]}-{cnic[12:]}"
                        cnic = formatedcnic
                    check_cnic = [i for i in Member.member_data if i["CNIC No"] == cnic]
                    if len(check_cnic) > 0:
                        print("\nMember with this cnic number already exists!\n")
                        continue
                    member_dict["CNIC No"] = cnic
                    Member.update()
                    print(f"\nCNIC updated successsfully to {cnic}.\n")
                    input("Press enter to go back...\n")
                    break
            elif choice == 8:
                print("Update member's roll number:")
                while True:
                    rollno = input("New Roll Number: ").strip()
                    roll_pattern = r"^[a-zA-Z0-9_.-]{1,15}$"
                    if not re.match(roll_pattern, rollno):
                        print(
                            "\nInvalid roll number! please enter valid roll number.\n"
                        )
                        continue
                    check_roll = [
                        i for i in Member.member_data if i["Roll No"] == rollno
                    ]
                    if len(check_roll) > 0:
                        print("\nMember with this roll number already exists!\n")
                        continue
                    member_dict["Roll No"] = rollno
                    Member.update()
                    print(f"\nRoll number successfully updated to {rollno}\n")
                    input("Press enter to go back...\n")
                    break
            elif choice == 9:
                print("Update member's department:")
                while True:
                    dept = input("New Department: ").strip().title()
                    dept_pattern = r"^[a-zA-Z\s.&-]+$"
                    if not re.match(dept_pattern, dept):
                        print("\nPlease enter a correct department name!\n")
                        continue
                    member_dict["Department"] = dept
                    Member.update()
                    print(f"\nDepartment successfully updated to {dept}.\n")
                    input("Press enter to go back...\n")
                    break
            elif choice == 10:
                print("Update member's University:")
                while True:
                    university = input("University name: ").strip().title()
                    if not re.match(dept_pattern, university):
                        print("\nPlease enter correct university name!\n")
                        continue
                    member_dict["University"] = university
                    Member.update()
                    print(f"\nUniversity successfully updated to {university}.\n")
                    input("Press enter to go back...\n")
                    break
            elif choice == 11:
                print("Update member's status:")
                while True:
                    status = (
                        input("Update member's status to [Block/Unblock]: ")
                        .strip()
                        .title()
                    )
                    if status == "Block":
                        if member_dict["Status"] == "Blocked":
                            print("\nMember already blocked!\n")
                            input("Press enter to go back...\n")
                            break
                        member_dict["Status"] == "Blocked"
                    elif status == "Unblock":
                        if member_dict["Status"] == "Active":
                            print("\nMember already active/unblock!\n")
                            input("Press enter to go back...\n")
                            break
                        member_dict["Status"] = "Active"
                    else:
                        print("\nInvalid Input!\n")
                        continue

                    Member.update()
                    print(f"\nStatus updated successfully to {status}.\n")
                    input("Press enter to go back...\n")
                    break

    def delete_member(self):
        print("     DELETE MEMBER\n", "-" * 37)
        while True:
            member_id = input("Enter Member-ID you want to delete: ").strip()
            id_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
            if len(id_check) == 0:
                print("User not found!")
                continue
            member_dict = id_check[0]
            index = Member.member_data.index(member_dict)
            Member.member_data.pop(index)
            Member.update()
            print("\nMember's account deleted successfully\n")
            input("Press enter to go back...\n")
            break

    def block_unblock_member(self):
        print("     BLOCK/UNBLOCK MEMBER\n", "-" * 37)
        while True:
            member_id = input("Enter Member-ID you want to delete: ").strip()
            id_check = [i for i in Member.member_data if i["Member-ID"] == member_id]
            if len(id_check) == 0:
                print("User not found!")
                continue
            break
        member_dict = id_check[0]
        while True:
            status = input("Block/Unblock: ").strip()
            if status == "Block" or status == "block":
                if member_dict["Status"] == "Blocked":
                    print("\nMember already blocked!\n")
                    input("Press enter to go back...\n")
                    break
                else:
                    member_dict["Status"] = "Blocked"
                    print("\nMember blocked successfully!\n")
                    Member.update()
                    input("Press enter to go back...\n")
                    break
            elif status == "Unblock" or status == "unblock":
                if member_dict["Status"] == "Active":
                    print("\nMember already active/unblocked\n")
                    input("Press enter to go back...\n")
                    break
                else:
                    member_dict["Status"] = "Active"
                    print("\nMember unblocked successfully!\n")
                    input("Press enter to go back...\n")
                    Member.update()
                    break
