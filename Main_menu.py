from Admin_login import admin_login
from User_Menu import user_menu
from state import state
from admin_menu import view_admin_menu
import sys
from Choice import get_choice

def main_menu():

    while True:
        print("====================")
        print("Airline Management System")
        print("====================")
        print("1--> Admin")
        print("2--> User")
        print("3--> Exit")
        try:
            choice = get_choice()

        except KeyboardInterrupt:
            sys.exit()

        if choice == 1:
            if not state.isLoggedIn:
                admin_login()
            else:
                view_admin_menu()
        elif choice == 2:
            user_menu()
        elif choice == 3:
            print("Bye 👋👋")
            break
        else:
            print("Wrong Choice")

# def main():
#     while True:
#         try:
#             choice = int(input("Enter your choice..."))
#         except ValueError:
#             print("Enter integer values only")
#             continue

#         if choice == 1:
#             if not state.isLoggedIn:
#                 admin_login()
#             else:
#                 view_admin_menu()
#         elif choice == 2:
#             user_menu()
#         elif choice == 3:
#             print("Bye 👋👋")
#             break
#         else:
#             print("Wrong Choice")

# if __name__ == '__main__':
#     main()

# from Admin_login import admin_login
# from User_Menu import user_menu
# from state import state
# from admin_menu import view_admin_menu

# def main_menu():
#     print("====================")
#     print("Airline Management System")
#     print("====================")
#     print("1--> Admin")
#     print("2--> User")
#     print("3--> Exit")

# def main():
#     while True:
#         main_menu()
#         try:
#             choice = int(input("Enter your choice..."))
#         except ValueError:
#             print("Enter integer values only")
#             continue

#         if choice == 1:
#             admin_login()
#         elif choice == 2:
#             user_menu()
#         elif choice == 3:
#             print("Bye 👋👋")
#             break
#         else:
#             print("Wrong Choice")

# if __name__ == '__main__':
#     main()