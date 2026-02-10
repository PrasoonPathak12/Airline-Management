from userSignUp import usersignup
def user_menu():
    # import admin_login() from 'admin_login.py'


    print("====================")
    print("Airline Management System")
    print("====================")

    print("1--> User Registration(Sign Up)")
    print("2--> User Login")
    print("3--> Exit")

def main():

    choice=int(input("Enter your choice: "))
    if choice not in (1,2,3):
        print("Wrong Choice")
    else:
        if choice == 1:
            usersignup()
        elif choice == 2:
            user_menu()
        else:
            print("Bye 👋👋")
