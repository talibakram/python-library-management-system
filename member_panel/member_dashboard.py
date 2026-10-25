# Base Class Import
from core.member_base import Member
# all classes import
from member_panel.member_auth import MemberAuthMixin
from member_panel.member_profile import MemberProfileMixin
from member_panel.book_discovery import BookSearchMixin
from member_panel.transactions import MemberTransactionsMixin
from member_panel.history_views import MemberViewsMixin
from member_panel.finances import MemberFinancesMixin

# Multiple Inheritance!
class MemberDashboard(Member, MemberAuthMixin, MemberProfileMixin, BookSearchMixin, MemberTransactionsMixin, MemberViewsMixin, MemberFinancesMixin):
    def member_dashboard(self):
        while True:
            print("\n" + "="*50)
            print(" "*18 + "MEMBER DASHBOARD")
            print("="*50)
            print("1. View Profile Details")
            print("2. Edit Details")
            print("3. Search Books")
            print("4. Reserve Book")
            print("5. Issue Book")
            print("6. Return Book")
            print("7. View Issued Books")
            print("8. View Reserved Books")
            print("9. Pay Fine")
            print("10. View Fine History")
            print("0. Logout")

            while True:
                try:
                    choice = int(input("\nEnter your choice: "))
                except ValueError:
                    print("\nInvalid input! input must be in digits.\n")
                    continue
                break
            if choice == 0:
                print("\nLogging out...")
                break

            elif choice == 1:
                self.view_profile()

            elif choice == 2:
                self.edit_details()

            elif choice == 3:
                self.search_books()

            elif choice == 4:
                self.reserve_book()

            elif choice == 5:
                self.issue_book()

            elif choice == 6:
                self.return_book()

            elif choice == 7:
                self.view_issued_books()

            elif choice == 8:
                self.view_reserved_books()
            
            elif choice == 9:
                self.pay_fine()
            
            elif choice == 10:
                self.view_fine_history()

            else:
                print("\nInvalid input! Please try again.\n")