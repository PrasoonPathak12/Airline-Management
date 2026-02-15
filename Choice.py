def get_choice():
    try:
        choice=int(input("Enter your choice..."))
        return choice
    except ValueError:
        print("Enter correct values only...")