# import admin_login() from 'admin_login.py'

from Admin_login import admin_login
from User_Menu import user_menu

def main_menu():
    print("====================")
    print("Airline Management System")
    print("====================")

    print("1--> Admin")
    print("2--> User")
    print("3--> Exit")

def main():
    main_menu()
    choice=int(input("Enter your choice: "))
    if choice not in (1,2,3):
        print("Wrong Choice")
    else:
        if choice == 1:
            admin_login()
        elif choice == 2:
            user_menu()
        else:
            print("Bye 👋👋")
main()