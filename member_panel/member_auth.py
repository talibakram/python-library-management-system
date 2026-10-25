
from datetime import datetime, timedelta
from pathlib import Path
import re
from core.member_base import Member  # VIP Engine Import

class MemberAuthMixin:
    def create_account(self):
        print("\n" + "="*50)
        print(" "*14 + "CREATE NEW ACCOUNT")
        print("="*50)

        while True:
            print("Enter your details below:\n")
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
                    print("\nAge must be 16 or 16+!\n")
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
                    print("\nInvalid CNIC number! Please enter a valid CNIC number.\n")
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
                    "Reserved Books": [],
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

    def member_login(self):
        print("\n" + "="*50)
        print(" "*18 + "MEMBER LOGIN")
        print("="*50)
        while True:
            member_id = input("Enter your Member-ID: ")
            password = input("Enter your password: ")
            details = [
                i
                for i in Member.member_data
                if i["Password"] == password
                and i["Member-ID"] == member_id
            ]
            if len(details) == 0:
                print("Invalid Credentials! Try Again.")
                continue
            else:
                # Set the logged-in member
                self.current_user = details[0]
                print(f"Login Successful! Welcome {details[0]['Name']}")
                break
        self.update()
        return True