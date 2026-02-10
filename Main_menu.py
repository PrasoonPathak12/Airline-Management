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
    while True:
        main_menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            admin_login()
        elif choice == 2:
            user_menu()
        elif choice == 3:
            print("Bye 👋👋")
            break
        else:
            print("Wrong Choice")

if __name__ == "__main__":
    main()
