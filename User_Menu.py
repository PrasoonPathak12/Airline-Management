from userSignUp import usersignup
from userLogin import user_login
from Choice import get_choice
import sys

def user_menu():
    while True:
        print("====================")
        print("User Menu")
        print("====================")
        print("1--> User Registration (Sign Up)")
        print("2--> User Login")
        print("3--> Back")

        try:
            choice = get_choice()
        except KeyboardInterrupt:
            sys.exit()

        if choice == 1:
            usersignup()
        elif choice == 2:
            user_login()
        elif choice == 3:
            break
        else:
            print("Wrong Choice")
