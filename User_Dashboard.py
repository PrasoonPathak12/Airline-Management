from state import state
import bcrypt
import pwinput
import sqlite3 as sql
from rich.console import Console
from rich.table import Table
from booking import initiate_booking
import sys

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

    def view_bookings():
        conn = sql.connect('airline.db')
        cursor = conn.cursor()
        console = Console()

        try:
            cursor.execute("""
                SELECT 
                    booking_id,
                    source,
                    destination,
                    departure_date,
                    return_date,
                    no_of_passengers,
                    total_price,
                    status,
                    booking_date,
                    seat_type
                FROM Bookings
                WHERE user_name = ?
                ORDER BY booking_id DESC
            """, (state.user_name,))

            bookings = cursor.fetchall()

            if not bookings:
                print("❌ No bookings found.")
                return

            table = Table(title="Your Bookings")

            table.add_column("Booking ID", style="cyan")
            table.add_column("Route", style="green")
            table.add_column("Departure", style="yellow")
            table.add_column("Return", style="yellow")
            table.add_column("Passengers", style="magenta")
            table.add_column("Total Price", style="blue")
            table.add_column("Status", style="red")
            table.add_column("Booked On", style="white")
            table.add_column("Seat Type", style="yellow")

            for booking in bookings:
                route = f"{booking[1]} → {booking[2]}"
                table.add_row(
                    str(booking[0]),
                    route,
                    booking[3],
                    booking[4] if booking[4] else "-",
                    str(booking[5]),
                    f"₹{booking[6]:.2f}",
                    booking[7],
                    booking[8],
                    booking[9]
                )

            console.print(table)

        except Exception as e:
            print(f"❌ Error fetching bookings: {e}")

        finally:
            conn.close()

    def cancel_ticket():
        conn = sql.connect('airline.db')
        cursor = conn.cursor()

        try:
            # First show bookings
            view_bookings()

            booking_id = input("\nEnter Booking ID to cancel (or press Enter to exit): ").strip()

            if booking_id == "":
                return

            if not booking_id.isdigit():
                print("❌ Invalid Booking ID.")
                return

            cursor.execute("""
                SELECT status 
                FROM Bookings
                WHERE booking_id = ? AND user_name = ?
            """, (booking_id, state.user_name))

            booking = cursor.fetchone()

            if not booking:
                print("❌ Booking not found.")
                return

            if booking[0] == "cancelled":
                print("⚠️ Booking already cancelled.")
                return

            confirm = input("Are you sure you want to cancel this booking? (y/n): ").lower()

            if confirm != 'y':
                print("Cancellation aborted.")
                return

            cursor.execute("""
                UPDATE Bookings
                SET status = 'cancelled'
                WHERE booking_id = ? AND user_name = ?
            """, (booking_id, state.user_name))

            # RESTORE THE FLIGHT SEATS AFTER CANCELLATION...

            cursor.execute("""
                SELECT flight_id,
                no_of_passengers,
                seat_type FROM Bookings
                WHERE user_name=? AND booking_id=?
            """,(state.user_name,booking_id))

            result=cursor.fetchone()

            if not result:
                print("❌ Booking not found.")
                return
            
            flight_id=result[0]
            passengers=result[1]
            seat_type=result[2]

            if seat_type.lower() == "business":
                cursor.execute("""
                UPDATE Flights 
                SET business_available_seats = business_available_seats+?
                WHERE flight_id=?
                """,(passengers,flight_id))
            else:
                cursor.execute("""
                UPDATE Flights 
                SET economy_available_seats =economy_available_seats + ?
                WHERE Bookings.flight_id=Flights.flight_id
                """,(passengers,flight_id))

            conn.commit()

            print("✅ Booking cancelled successfully.")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error cancelling booking: {e}")

        finally:
            conn.close()


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
        # print("8. Country")
        print("8. Zip Code")
        print("9. Cancel ❌❌")

        field_choice = input("\nEnter your choice (1-10): ")

        field_map = {
            "1": ("user_pass", "New Password"),
            "2": ("email_Id", "New Email"),
            "3": ("phone", "New Phone Number"),
            "4": ("address1", "New Address Line 1"),
            "5": ("address2", "New Address Line 2"),
            "6": ("city", "New City"),
            "7": ("state", "New State"),
            # "8": ("country", "New Country"),
            "8": ("zipcode", "New Zip Code")
        }

        if field_choice == "9":
            try:
                print("🛑🛑Update cancelled.")
                return
            except KeyboardInterrupt:
                print("⚠️⚠️⚠️Exiting program....")
                sys.exit()
        
        

        if field_choice not in field_map:
            print("❌ Invalid choice")
            return

        column_name, prompt = field_map[field_choice]

        if column_name=="city":
            try:
                new_value = input("Enter City ➜ ").strip()
                if not new_value.isalpha():
                    print("🛑🛑🛑City can only be alphabetic")
                    return
                # print("City cannot be empty.")
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("⚠️⚠️⚠️Exiting the application....")

        if column_name=="state":
            states = [
                    "andhra pradesh","arunachal pradesh",
                    "assam","bihar","chandigarh",
                    "chhattisgarh","delhi","goa",
                    "gujarat","haryana","himachal pradesh",
                    "jharkhand","karnataka","kerala","madhya pradesh",
                    "maharashtra","manipur",
                    "meghalaya","mizoram",
                    "nagaland","odisha",
                    "punjab","rajasthan",
                    "sikkim","tamil nadu",
                    "telangana","tripura",
                    "uttar pradesh","uttarakhand","west bengal"
            ]

        if column_name=="state":
            try:
                value=input(f"Enter {prompt}: ")
                if value not in states:
                    print("Enter valid indian states...")
                    return
                new_value = value.lower()
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("⚠️⚠️⚠️Exiting program....")
                sys.exit()

        if column_name == "phone":
            try:
                value = input(f"Enter {prompt}: ")
                if value.isdigit() and len(value) == 10 and value[0] in ('6','7','8','9'):
                    new_value=int(value)
                else:
                    print("❌❌Invalid Indian phone number.")
                    return
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("⚠️⚠️⚠️Exiting program....")
                sys.exit()

        # Convert to integer for phone and zipcode
        if column_name == "zipcode":
            try:
                value = input(f"Enter {prompt}: ")
                if(len(value)==6 and value.isdigit() and int(value[0])>=1):
                    # print("Only valid code...")    
                    new_value= int(value)
                else:
                    print("🛑🛑Enter valid zip values starting with 1-9 and length of 6...")
                    return

            except ValueError:
                print("❌ Invalid input. Must be a number.")
                return
            except KeyboardInterrupt:
                    print("⚠️⚠️⚠️Exiting program....")
                    sys.exit()
        
        if column_name=="user_pass":
            try:
                value = pwinput.pwinput(prompt="Enter user password: ", mask='*').replace(" ", "")
                if not 8 <= len(value) <= 14:
                    print("Password length must be 8–14 characters.")
                    return
                new_value=bcrypt.hashpw(value.encode(), bcrypt.gensalt())
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("⚠️⚠️⚠️Exiting program...")
        
        # Confirm update
        try:
            confirm = input(f"\nConfirm update of {prompt} to '{new_value}'? (y/n): ")
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting program....")
            sys.exit()
        
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
        print("4--> View bookings")
        print("5--> Cancel bookings")
        print("6--> Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Profile details shown here")
            view_profile()
        elif choice == "2":
            update_profile()
        elif choice == "3":
            print("Flight booking screen")
            initiate_booking()
        elif choice == "4":
            print("Viewing Bookings...")
            view_bookings()
        elif choice=="5":
            print("Loading Cancel booking options....")
            cancel_ticket()
        elif choice == "6":
            print("Logging out...")
            state.isLoggedIn=False
            break   # EXIT dashboard
        else:
            print("Invalid choice")
