# Base Class
from core.admin_base import Admin
from core.book_model import Book

# Imported all Mixin Classes
from admin_panel.admin_auth import AdminAuthMixin
from admin_panel.manage_members import ManageMembersMixin
from admin_panel.manage_books import ManageBooksMixin
from admin_panel.book_circulation import AdminCirculationMixin
from admin_panel.finances import AdminFinancesMixin
from admin_panel.reports import ReportsSystemMixin
from admin_panel.system_management import SystemManagementMixin


class AdminDashboard(Admin, AdminAuthMixin, ManageMembersMixin, ManageBooksMixin, AdminCirculationMixin, AdminFinancesMixin, ReportsSystemMixin, SystemManagementMixin):
    def admin_dashboard(self):
        while True:
            print("=" * 37)
            print("         ADMIN MENU")
            print("=" * 37)

            print("1. SECURITY")
            print("2. MEMBER MANAGEMENT")
            print("3. BOOK MANAGEMENT")
            print("4. BOOK CIRCULATION")
            print("5. FINE MANAGEMENT")
            print("6. MONITORING & REPORTS")
            print("7. SYSTEM MANAGEMENT")
            print("0. LOGOUT")

            try:
                choice = int(input("Enter your response: "))

            except ValueError:
                print("Response must be in digits!")
                continue

            if choice == 1:
                while True:
                    print("     SECURITY\n", "-" * 37)
                    print("1. Change Password")
                    print("2. Update Details")
                    print("0. Back")
                    try:
                        choice2 = int(input("Enter your response: "))
                    except ValueError:
                        print("Response must be in digits!")
                        continue

                    if choice2 == 1:
                        self.changepassword()

                    elif choice2 == 2:
                        print("\n     UPDATE DETAILS\n", "-" * 37)
                        print("You can update the below details:")
                        while True:
                            print("1. Update Name")
                            print("2. Update Email")
                            print("3. Update Phone Number")
                            print("4. Update Username")
                            print("0. Back")
                            try:
                                subchoice = int(input("Enter your response: "))
                            except ValueError:
                                print("Response must be in digits!")
                                continue
                            if subchoice == 0:
                                break
                            elif subchoice == 1:
                                self.updatename()
                            elif subchoice == 2:
                                self.updateemail()
                            elif subchoice == 3:
                                self.updatephone()
                            elif subchoice == 4:
                                self.updateusername()
                            else:
                                print("Invalid Input! Try again")

                    elif choice2 == 0:
                        break
                    else:
                        print("Invalid Input! Try Again.")

            elif choice == 2:
                print("\n      MEMBER MANAGEMENT\n", "-" * 37)
                while True:
                    print("\n1. Register New Member")
                    print("2. View Member Details")
                    print("3. Update Member Details")
                    print("4. Delete Member")
                    print("5. Block/Unblock Member")
                    print("0. Back")
                    try:
                        choice3 = int(input("Enter your response (0-5): "))
                    except ValueError:
                        print("Response must be in digits!")
                        continue

                    if choice3 == 1:
                        self.addmember()
                    elif choice3 == 2:
                        self.view_memberdetails()
                    elif choice3 == 3:
                        self.update_member_details()
                    elif choice3 == 4:
                        self.delete_member()
                    elif choice3 == 5:
                        self.block_unblock_member()
                    elif choice3 == 0:
                        break
                    else:
                        print("Invalid Input! Try Again.")

            elif choice == 3:
                while True:
                    print("\n       BOOK MANAGEMENT\n", "-" * 37)
                    print("1. Add New Book")
                    print("2. Search Books")
                    print("3. Update Book Details")
                    print("4. Delete Book")
                    print("5. Manage Book Categories")
                    print("0. Back")
                    while True:
                        try:
                            choice4 = int(input("Enter your response: "))
                        except ValueError:
                            print("response must be in digits!")
                            continue
                        break
                    if choice4 == 1:
                        print("\n       ADD NEW BOOK\n", "-" * 37)
                        while True:
                            print("Enter some book details below to add book:")
                            title = input("Book Title: ").strip().title()
                            author = input("Author Name: ").strip().title()
                            book_check = [
                                i
                                for i in Book.book_data
                                if i["Title"] == title and i["Author"] == author
                            ]
                            if len(book_check) > 0:
                                print(
                                    f"\nBook {title} by {author} is already in library!\n"
                                )
                                continue
                            category = input("Book Category: ").strip().title()
                            Book(title, author, category)
                            print(f"\nBook [{title}] successfully added to library.\n")
                            input("Press enter to go back...\n")
                            break

                    elif choice4 == 2:
                        self.view_all_books()

                    elif choice4 == 3:
                        self.update_book_details()
                    elif choice4 == 4:
                        self.delete_book()
                    elif choice4 == 5:
                        self.manage_categories()
                    elif choice4 == 0:
                        break
                    else:
                        print("Invalid Input! Try Again.")

            elif choice == 4:
                while True:
                    print("\n       BOOK CIRCULATION\n", "-" * 37)
                    print("1. Issue a Book")
                    print("2. Return a Book")
                    print("3. Manage Reservations")
                    print("0. Back")
                    try:
                        choice5 = int(input("Enter your response: "))
                    except ValueError:
                        print("Response must be in digits!")
                        continue
                    if choice5 == 1:
                        self.issue_book()
                    elif choice5 == 2:
                        self.return_book()
                    elif choice5 == 3:
                        self.manage_reservations()
                    elif choice5 == 0:
                        break
                    else:
                        print("Invalid Input! Try Again.")

            elif choice == 5:
                while True:
                    print("\n       FINE MANAGEMENT\n", "-" * 37)
                    print("1. View Unpaid Fines")
                    print("2. Record Fine Payment")
                    print("0. Back")
                    try:
                        choice6 = int(input("Enter your response: "))
                    except ValueError:
                        print("Response must be in digits!")
                        continue
                    if choice6 == 1:
                        self.view_unpaid_fines()
                    elif choice6 == 2:
                        self.record_fine_payment()
                    elif choice6 == 0:
                        break
                    else:
                        print("Invalid Input! Try Again.")
            elif choice == 6:
                while True:
                    print("\n       MONITORING & REPORTS\n", "-" * 37)
                    print("1. View Overdue Books")
                    print("2. View Library Dashboard")
                    print("3. View Reports")
                    print("4. View Activity Logs")
                    print("0. Back")
                    try:
                        choice7 = int(input("Enter your response: "))
                    except ValueError:
                        print("Response must be in digits!")
                        continue
                    if choice7 == 1:
                        self.view_overdue_books()
                    elif choice7 == 2:
                        self.view_library_dashboard()
                    elif choice7 == 3:
                        self.view_reports()
                    elif choice7 == 4:
                        self.view_activity_logs()
                    elif choice7 == 0:
                        break
                    else:
                        print("Invalid Input! try Again.")

            elif choice == 7:
                while True:
                    print("\n       SYSTEM MANAGEMENT\n", "-" * 37)
                    print("1. Backup Data")
                    print("2. Restore Data")
                    print("0. Back")
                    try:
                        choice8 = int(input("Enter your response: "))
                    except ValueError:
                        print("Response must be in digits!")
                        continue
                    if choice8 == 1:
                        self.backup_data()
                    elif choice8 == 2:
                        self.restore_data()
                    elif choice8 == 0:
                        break
                    else:
                        print("Invalid Input! Try Again.")

            elif choice == 0:
                print("Logging Out...!")
                break
            else:
                print("Invalid Input! Try Again.")
