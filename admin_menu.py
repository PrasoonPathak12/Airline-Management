from Inventory import manage_inventory
from users import manage_users

def view_admin_menu():
    while True:
        print("=============================")

        print("1 ---> Manage Inventory")
        print("2 ---> Manage USERS")

        print("What action to take? \n")
        choice=int(input("Choose 1 or 2 :"))
        if choice not in (1,2):
            print("Make choice from available options...")
            continue
        else:
            if choice==1:
                manage_inventory()
            elif choice == 2:
                manage_users()
            else:
                break
        return
