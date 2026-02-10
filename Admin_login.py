from admin_menu import view_admin_menu
from state import state

ADMIN_USER_ID="admin"
ADMIN_PASSWORD = "admin"

def admin_login():
    print("\n<---Admin Sign In--->")
    admin_user_id = input("Enter admin user Id: \n")
    admin_password = input("Enter your admin password: \n")
    if ADMIN_USER_ID==admin_user_id and ADMIN_PASSWORD==admin_password:
        print("\n\n=====Admin logged in successfully=====\n\n")
        state.isLoggedIn = True
        view_admin_menu()
    else:
        print("You may have entered wrong credentials...Please try again\n\n")