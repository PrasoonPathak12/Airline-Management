import sqlite3
from rich.console import Console
from rich.table import Table

def manage_inventory():

    conn = sqlite3.connect("airline.db")
    cursor = conn.cursor()

    def insert_carrier_details():
        carrier_id = int(input("Enter Carrier ID: "))
        carrier_name = input("Enter Carrier Name: ")

        refund_2 = int(input("Refund % before 2 days: "))
        refund_10 = int(input("Refund % before 10 days: "))
        refund_20 = int(input("Refund % before 20 days: "))

        silver_discount = int(input("Silver user discount %: "))
        gold_discount = int(input("Gold user discount %: "))

        flight_id = int(input("Enter Flight ID: "))

        # Check if flight exists
        cursor.execute(
            "SELECT flight_id FROM Flights WHERE flight_id = ?",
            (flight_id,)
        )
        flight = cursor.fetchone()

        if not flight:
            print("⚠️ Flight does not exist. Creating new flight entry.")

            flight_name = input("Enter Flight Name: ")
            start_loc = input("Enter Start Location: ")
            end_loc = input("Enter End Location: ")

            cursor.execute(
                """
                INSERT INTO Flights (flight_name, start_loc, end_loc)
                VALUES (?, ?, ?)
                """,
                (flight_name, start_loc, end_loc)
            )
            conn.commit()
            print("✅ Flight created successfully.")

        # Insert carrier
        cursor.execute(
            """
            INSERT INTO Carriers (
                Carrier_Id,
                Carrier_name,
                refund_before_2days_Of_travel,
                refund_before_10days_Of_travel,
                refund_before_20days_Of_travel,
                silver_user_discount,
                gold_user_discount,
                flight_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                carrier_id,
                carrier_name,
                refund_2,
                refund_10,
                refund_20,
                silver_discount,
                gold_discount,
                flight_id
            )
        )

        conn.commit()
        print("✅ Carrier inserted successfully.")

    def remove_carrier_details():
        cursor.execute("SELECT * FROM Carriers")
        carrier_details = cursor.fetchall()

        table = Table(title="Carriers Data")

        columns = [desc[0] for desc in cursor.description]
        for col in columns:
            table.add_column(col, style="cyan")

        for carrier in carrier_details:
            table.add_row(*map(str, carrier))

        console = Console()
        console.print(table)
        
        carrier_id = int(input("Enter Carrier ID to remove: "))

        cursor.execute(
            """
            DELETE FROM Carriers
            WHERE Carrier_Id = ?
            """,
            (carrier_id,)
        )

        if cursor.rowcount == 0:
            print("❌ No carrier found with given Carrier ID and Flight ID.")
        else:
            conn.commit()
            print("✅ Carrier removed successfully.")

        confirmation_msg = input("Do you want to continue removing other carriers as well? Enter y for yes, n for No: ")
        if confirmation_msg.lower() == 'y':
            return True
        elif confirmation_msg.lower() == 'n':
            return False
        else:
            return False

    while True:
        print("\n--- Manage Inventory ---")
        print("1. Insert Carrier Details")
        print("2. Remove Carrier Details")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            insert_carrier_details()
        elif choice == "2":
            while True:
                msg = remove_carrier_details()
                if msg == False:
                    break
        else:
            print("❌ Invalid choice")
            break

    conn.close()
