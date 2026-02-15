from admin_menu import view_admin_menu
from state import state
import pwinput
import sys

ADMIN_USER_ID="admin"
ADMIN_PASSWORD = "admin"

def admin_login():
    attempts=3
    while attempts>0:
        try:
            print("\n<---Admin Sign In--->")
            admin_user_id = input("Enter admin user Id: \n")
            admin_password = pwinput.pwinput(prompt="Enter admin password: ", mask='*')
            if ADMIN_USER_ID==admin_user_id and ADMIN_PASSWORD==admin_password:
                print("\n\n=====✅✅✅Admin logged in successfully=====\n\n")
                state.isLoggedIn = True
                view_admin_menu()
                return
            else:
                attempts-=1
                print("⌚⌚⌚⌚⌚⌚")
                print(f"You may have entered wrong credentials... '{attempts}' Attempts remaining\n\n")

        except KeyboardInterrupt:
            print("Exiting Program...⚠️")
            sys.exit()
        except Exception as e:
            print(e)
    print("🚫❌❌❌ Maximum login attempts reached. Access denied.")
    sys.exit()