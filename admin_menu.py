# from Inventory import manage_inventory
# from users import manage_users

# def view_admin_menu():
#     print("=============================")

#     print("1 ---> Manage Inventory")
#     print("2 ---> Manage USERS")
#     print("3----> Exit")

#         try:
#             while True:
#                 print("What action to take? \n")
#                 choice = get_choice()        
#                 if choice==1:
#                     manage_inventory()  
#                 elif choice == 2:
#                     manage_users()
#                 elif choice == 3:
#                     main_menu()
        
        
        
#         except KeyboardInterrupt:
#             break
        
#         if choice not in (1,2):
#             print("Make choice from available options...")
#         else:
#             if choice==1:
#                 manage_inventory()  
#             elif choice == 2:
#                 manage_users()
#             else:
#                 break
    # return
from Choice import get_choice
import sys
from Inventory import manage_inventory
from users import manage_users
from Choice import get_choice
from state import state

def view_admin_menu():
    try:
        while True:
            print("=============================")

            print("1 ---> Manage Inventory")
            print("2 ---> Manage USERS")
            print("3 ---> Back")

            print("What action to take? \n")
            
            choice = get_choice()
            
            if choice not in (1,2,3):
                print("Make choice from available options...")
                continue
            else:
                if choice==1:
                    manage_inventory()   
                elif choice == 2:
                    manage_users()
                elif choice == 3 :
                    state.isLoggedIn=False
                    break
        return
    except KeyboardInterrupt:
        print("\nExiting Program...⚠️")
        sys.exit()