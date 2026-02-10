from state import state
import sqlite3 as sql
from rich.console import Console
from rich.table import Table

def userDashboard():
    conn = sql.connect('airline.db')
    cursor = conn.cursor()

    def view_profile():
        cursor.execute(
            "SELECT * FROM Users WHERE user_name = ?",
            (state.user_name,)
        )

        user_info = cursor.fetchall()

        table = Table(title="User Information")

        columns = [desc[0] for desc in cursor.description]
        for col in columns:
            table.add_column(col, style="cyan")

        for user in user_info:
            table.add_row(*map(str, user))

        console = Console()
        console.print(table)

    def update_profile():
        print("\n=== UPDATE PROFILE ===\n")

        view_profile()

        print("\nWhich field would you like to update?")
        print("1. Password")
        print("2. Email")
        print("3. Phone")
        print("4. Address Line 1")
        print("5. Address Line 2")
        print("6. City")
        print("7. State")
        print("8. Country")
        print("9. Zip Code")
        print("10. Cancel")

        field_choice = input("\nEnter your choice (1-10): ")

        field_map = {
            "1": ("user_pass", "New Password"),
            "2": ("email_Id", "New Email"),
            "3": ("phone", "New Phone Number"),
            "4": ("address1", "New Address Line 1"),
            "5": ("address2", "New Address Line 2"),
            "6": ("city", "New City"),
            "7": ("state", "New State"),
            "8": ("country", "New Country"),
            "9": ("zipcode", "New Zip Code")
        }

        if field_choice == "10":
            print("Update cancelled.")
            return

        if field_choice not in field_map:
            print("❌ Invalid choice")
            return

        column_name, prompt = field_map[field_choice]
        new_value = input(f"Enter {prompt}: ")

        # Convert to integer for phone and zipcode
        if column_name in ["phone", "zipcode"]:
            try:
                new_value = int(new_value)
            except ValueError:
                print("❌ Invalid input. Must be a number.")
                return
        
        # Confirm update
        confirm = input(f"\nConfirm update of {prompt} to '{new_value}'? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Update cancelled.")
            return
        
        # Update the database
        cursor.execute(
            f"UPDATE Users SET {column_name} = ? WHERE user_name = ?",
            (new_value, state.user_name)
        )
        
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Profile updated successfully!")
            
            # Show updated profile
            print("\nUpdated Profile:")
            view_profile()
        else:
            print("❌ Update failed. User not found.")

    while True:
        print("USER DASHBOARD")
        print("====================")
        print("1--> View Profile")
        print("2--> Update Profile")
        print("3--> Book Flight")
        print("4--> Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Profile details shown here")
            view_profile()
        elif choice == "2":
            update_profile()
        elif choice == "3":
            print("Flight booking screen")
        elif choice == "4":
            print("Logging out...")
            break   # EXIT dashboard
        else:
            print("Invalid choice")
