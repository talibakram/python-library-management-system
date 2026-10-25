# File: main.py


from admin_panel.admin_dashboard import AdminDashboard
from member_panel.member_dashboard import MemberDashboard

def main_gate():
    
    admin_system = AdminDashboard()
    member_system = MemberDashboard()

    while True:
        print("\n" + "=" * 50)
        print(" "*10 + "📚 LIBRARY MANAGEMENT SYSTEM 📚")
        print("=" * 50)
        print("1. Admin Portal")
        print("2. Student (Member) Portal")
        print("0. Exit Application")
        print("=" * 50)
        
        try:
            choice = int(input("\nEnter your choice (0-2): "))
        except ValueError:
            print("\nInvalid response! Please enter digits only.\n")
            continue

        if choice == 1:
            print("\n" + "=" * 37)
            print(" "*12 + "ADMIN LOGIN")
            print("=" * 37)
            
            # if login successful then open admin dashboard
            login_success = admin_system.admin_login()
            if login_success:
                admin_system.admin_dashboard()  # Admin loop started!
                
        elif choice == 2:
            while True:
                print("\n" + "="*50)
                print(" "*14 + "👥 MEMBER PORTAL MENU 👥")
                print("="*50)
                print("1. Create New Account")
                print("2. Member Login")
                print("0. Back to Main Menu")
                print("="*50)
                
                try:
                    mem_choice = int(input("\nEnter your choice: "))
                except ValueError:
                    print("\nResponse must be in digits!\n")
                    continue
                    
                if mem_choice == 0:
                    break
                    
                elif mem_choice == 1:
                    member_system.create_account()
                    
                elif mem_choice == 2:
                    login_success = member_system.member_login()
                    if login_success:
                        member_system.member_dashboard()  # Member loop started!
                else:
                    print("\nInvalid Choice! Try again.\n")
                    
        elif choice == 0:
            print("\nExiting Library Management System. Goodbye!\n")
            break
        else:
            print("\nInvalid Response! Try Again.\n")


if __name__ == "__main__":
    main_gate()

    