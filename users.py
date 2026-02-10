import sqlite3
from rich.console import Console
from rich.table import Table

def manage_users():
    conn = sqlite3.connect("airline.db")
    cursor = conn.cursor()

    def remove_user_details():
        cursor.execute("SELECT * FROM Users")
        user_details = cursor.fetchall()

        table = Table(title="Users Data")

        columns = [desc[0] for desc in cursor.description]
        for col in columns:
            table.add_column(col, style="cyan")

        for user in user_details:
            table.add_row(*map(str, user))

        console = Console()
        console.print(table)
        
        user_name = int(input("Enter Username to remove: "))

        cursor.execute(
            """
            DELETE FROM Users
            WHERE user_name = ?
            """,
            (user_name,)
        )

        if cursor.rowcount == 0:
            print("❌ No user found with given User ID.")
        else:
            conn.commit()
            print("✅ User removed successfully.")

        confirmation_msg = input("Do you want to continue removing other users as well? Enter y for yes, n for No: ")
        if confirmation_msg.lower() == 'y':
            return True
        elif confirmation_msg.lower() == 'n':
            return False
        else:
            return False

    while True:
        print("\n--- Manage Users ---")
        print("1. Remove User Details")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                msg = remove_user_details()
                if msg == False:
                    break
        elif choice == "2":
            print("Exiting user management...")
            break
        else:
            print("❌ Invalid choice")

    conn.close()