from userSignUp import usersignup
from userLogin import user_login

def user_menu():
    while True:
        print("====================")
        print("User Menu")
        print("====================")
        print("1--> User Registration (Sign Up)")
        print("2--> User Login")
        print("3--> Back")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            usersignup()
        elif choice == 2:
            user_login()
        elif choice == 3:
            break
        else:
            print("Wrong Choice")
