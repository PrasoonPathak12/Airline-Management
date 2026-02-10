def userDashboard():
    while True:
        print("USER DASHBOARD")
        print("====================")
        print("1--> View Profile")
        print("2--> Book Flight")
        print("3--> Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Profile details shown here")

        elif choice == "2":
            print("Flight booking screen")

        elif choice == "3":
            print("Logging out...")
            break   # EXIT dashboard

        else:
            print("Invalid choice")
