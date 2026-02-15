import sqlite3 as sql
from rich.console import Console
from rich.table import Table
from datetime import datetime
from state import state
import sys

def book_ticket(source, destination, date_from, date_to, no_of_passengers,seat_type):
    conn = sql.connect('airline.db')
    cursor = conn.cursor()
    console = Console()
    
    try:
        
        print(f"\n🔍 Searching flights from {source} to {destination}...\n")


        
#         cursor.execute("""
#     SELECT 
#         f.flight_id, 
#         f.flight_name, 
#         f.start_loc, 
#         f.end_loc,
#         c.carrier_id, 
#         c.carrier_name, 
#         c.silver_user_discount, 
#         c.gold_user_discount,
#         f.economy_available_seats,
#         f.business_available_seats,
#         f.base_price
#     FROM Flights f
#     JOIN Carriers c 
#         ON f.flight_id = c.flight_id
#     WHERE LOWER(f.start_loc) = LOWER(?) 
#     AND LOWER(f.end_loc) = LOWER(?)
# """, (source, destination))

        cursor.execute("""
            SELECT 
                f.flight_id, 
                f.flight_name, 
                f.start_loc, 
                f.end_loc,
                c.carrier_id, 
                c.carrier_name, 
                f.economy_available_seats,
                f.business_available_seats,
                f.base_price
            FROM Flights f
            JOIN Carriers c 
                ON f.flight_id = c.flight_id
            WHERE LOWER(f.start_loc) = LOWER(?) 
            AND LOWER(f.end_loc) = LOWER(?)
        """, (source, destination))

        
        available_flights = cursor.fetchall()
        # print(available_flights)
        if not available_flights:
            print(f"❌ No flights available from {source} to {destination}")
            return False
        
       
        table = Table(title=f"Available Flights: {source} → {destination}")
        table.add_column("Index", style="yellow")
        table.add_column("Flight ID", style="cyan")
        table.add_column("Flight Name", style="green")
        table.add_column("Carrier", style="magenta")
        table.add_column("Route", style="blue")
        table.add_column("Economy_available_seats", style="blue")
        table.add_column("Business_available_seats", style="blue")
        table.add_column("Base_Price", style="blue")
        

        
        for idx, flight in enumerate(available_flights, 1):
            route = f"{flight[2]} → {flight[3]}"
            table.add_row(
                str(idx),
                str(flight[0]),
                flight[1],
                flight[5],
                route,
                str(flight[6]),
                str(flight[7]),
                str(flight[8])
            )
        
        console.print(table)
        
        
        
        while True:
            try:
                flight_choice = int(input("\nSelect flight (enter index number): ")) - 1
                break
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt:
                print("Exiting application...")
        
            if flight_choice < 0 or flight_choice >= len(available_flights):
                print("❌ Invalid selection")
                continue
        
        selected_flight = available_flights[flight_choice]

        economy_available = selected_flight[6]
        business_available = selected_flight[7]
        flight_id = selected_flight[0]
        carrier_id = selected_flight[4]
        carrier_name = selected_flight[5]
        # silver_discount = selected_flight[6]
        # gold_discount = selected_flight[7]
        
        base_price=selected_flight[8]
        
       
        cursor.execute(
            "SELECT user_tier FROM Users WHERE user_name = ?",
            (state.user_name,)
        )
        user_data = cursor.fetchone()
        user_tier = user_data[0] if user_data else "regular"
        
        discount = 0
        if user_tier.lower() == "silver":
            # discount = silver_discount
            discount = 5
        elif user_tier.lower() == "gold":
            # discount = gold_discount
            discount = 7

        if seat_type == "economy":
            if economy_available < no_of_passengers:
                print("❌ Not enough economy seats available.")
                return False
        elif seat_type == "business":
            if business_available < no_of_passengers:
                print("❌ Not enough business seats available.")
                return False
        
        
        discounted_price = base_price * (1 - discount / 100)
        total_price = discounted_price * no_of_passengers
        
        
        print("\n" + "="*50)
        print("BOOKING SUMMARY")
        print("="*50)
        print(f"Flight: {selected_flight[1]} ({carrier_name})")
        print(f"Route: {source} → {destination}")
        print(f"Departure Date: {date_from}")
        if date_to:
            print(f"Return Date: {date_to}")
        print(f"Passengers: {no_of_passengers}")
        print(f"User Tier: {user_tier.upper()}")
        print(f"Base Price: ₹{base_price:.2f} per passenger")
        if discount > 0:
            print(f"Discount: {discount}%")
            print(f"Discounted Price: ₹{discounted_price:.2f} per passenger")
        print(f"Total Amount: ₹{total_price:.2f}")
        print("="*50)
        
       
        while True:
            try:
                confirm = input("\nConfirm booking? (y/n): ")
                if confirm not in('Y','N','y','n'):
                    print("Valid values only...")
                    continue
                break
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print("Exiting program...")
        
        if confirm not in('y','Y'):
            print("❌ Booking cancelled")
            return False
        
        # ================= REDUCE SEAT COUNT =================

        if seat_type == "economy":
            cursor.execute("""
                UPDATE Flights
                SET economy_available_seats = economy_available_seats - ?
                WHERE flight_id = ?
            """, (no_of_passengers, flight_id))

        else:
            cursor.execute("""
                UPDATE Flights
                SET business_available_seats = business_available_seats - ?
                WHERE flight_id = ?
            """, (no_of_passengers, flight_id))

        
        # state.seat_type=seat_type
        
        booking_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO Bookings (
                user_name, 
                flight_id, 
                carrier_id,
                source,
                destination,
                departure_date,
                return_date,
                no_of_passengers,
                base_price,
                discount_percent,
                total_price,
                booking_date,
                status,
                seat_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (
            state.user_name,
            flight_id,
            carrier_id,
            source,
            destination,
            date_from,
            date_to,
            no_of_passengers,
            base_price,
            discount,
            total_price,
            booking_date,
            'confirmed',
            seat_type
        ))
        
        booking_id = cursor.lastrowid
        
        conn.commit()
        
        # Step 9: Success message
        print("\n" + "🎉"*25)
        print(f"✅ BOOKING CONFIRMED!")
        print(f"Booking ID: {booking_id}")
        print(f"Total Amount Paid: ₹{total_price:.2f}")
        print("🎉"*25 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during booking: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

# Helper function for the user dashboard
def initiate_booking():
    print("\n" + "="*50)
    print("FLIGHT BOOKING")
    print("="*50)
    
    while True:
            try:
                source = input("Enter Start Location: ")
                if not source.isalpha():
                    print("Enter values from  A to Z and a to z ...")
                    continue
            
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
        
            try:
                destination = input("Enter end Location: ")
                if not destination.isalpha():
                    print("Enter values from  A to Z and a to z ...")
                    continue
            
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            if source==destination:
                print("CHOOSE WISELY 😒...Destination and source cannot be the same")
                continue
            break

    while True:
        try:
            trip_type=input("Enter type of trip, round or one-way as r/o: ")
            if trip_type not in('r','o','R','O'):
                continue
            break
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("EXITING PROGRAM")
            sys.exit()

 

    # ================= DEPARTURE DATE =================
    while True:
        try:
            date_from = input("Enter departure date (DD-MM-YYYY): ").strip()

            # Check format
            departure_date_obj = datetime.strptime(date_from, "%d-%m-%Y")

            # Remove time part for accurate comparison
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Check if departure is in future
            if departure_date_obj < today or departure_date_obj.year > today.year:
                print(f"❌ Departure date must be in the future and for the year {today.year} only")
                continue

            break

        except ValueError:
            print("❌ Invalid format! Please enter date as DD-MM-YYYY.")
        except KeyboardInterrupt:
            print("\nExiting application...")
            sys.exit()


    # ================= RETURN DATE =================
    date_to = None

    if trip_type == 'r':
        while True:
            try:
                date_to = input("Enter return date (DD-MM-YYYY): ").strip()

                return_date_obj = datetime.strptime(date_to, "%d-%m-%Y")

                # Check if return date is after departure
                if return_date_obj <= departure_date_obj:
                    print(f"❌ Return date must be after departure date and for the year {today.year} only")
                    continue

                break

            except ValueError:
                print("❌ Invalid format! Please enter date as DD-MM-YYYY.")
            except KeyboardInterrupt:
                print("\nExiting application...")
                sys.exit()


    
    while True:
        try:
            no_of_passengers = int(input("Enter number of passengers: "))
            break
        except Exception as e:
            print(e)
            continue
        except KeyboardInterrupt:
            sys.exit()
    
    while True:
        try:
            choice_of_seats = input("1 --> Business\n2 --> Economy\nChoose seat type: ")

            if choice_of_seats not in ("1", "2"):
                print("❌ Invalid choice")
                continue

            seat_type = "business" if choice_of_seats == "1" else "economy"
            break

        except Exception as e:
            print(e)

        except KeyboardInterrupt:
            print("⚠️ Exiting program...")
            sys.exit()


    
    if no_of_passengers <= 0:
        print("❌ Invalid number of passengers")
        return
    
    # Call the booking function
    # print("fff")
    book_ticket(source, destination, date_from,date_to, no_of_passengers,seat_type)

# book_ticket("Delhi","Mumbai","2026-12-02","2026-12-02",3)





# import sqlite3 as sql
# from rich.console import Console
# from rich.table import Table
# from datetime import datetime
# from state import state


# def book_ticket(source, destination, no_of_passengers):

#     conn = sql.connect("airline.db")
#     cursor = conn.cursor()
#     console = Console()

#     try:
#         print("\n" + "=" * 50)
#         print("SEARCHING AVAILABLE FLIGHTS")
#         print("=" * 50)

#         # ✅ Fetch flights with carrier details
#         cursor.execute("""
#             SELECT 
#                 f.flight_id,
#                 f.flight_name,
#                 f.start_loc,
#                 f.end_loc,
#                 f.base_price,
#                 f.economy_available_seats,
#                 f.business_available_seats,
#                 c.carrier_id,
#                 c.carrier_name,
#                 c.silver_user_discount,
#                 c.gold_user_discount
#             FROM Flights f
#             JOIN Carriers c
#                 ON f.carrier_id = c.carrier_id
#             WHERE LOWER(f.start_loc) = LOWER(?)
#             AND LOWER(f.end_loc) = LOWER(?)
#         """, (source, destination))

#         flights = cursor.fetchall()

#         if not flights:
#             print("❌ No flights available for this route.")
#             return False

#         # ✅ Display flights
#         table = Table(title=f"{source} → {destination} Flights")
#         table.add_column("Index", style="yellow")
#         table.add_column("Flight ID", style="cyan")
#         table.add_column("Flight Name", style="green")
#         table.add_column("Carrier", style="magenta")
#         table.add_column("Base Price", style="red")
#         table.add_column("Eco Seats", style="blue")
#         table.add_column("Bus Seats", style="blue")

#         for idx, flight in enumerate(flights, 1):
#             table.add_row(
#                 str(idx),
#                 str(flight[0]),
#                 flight[1],
#                 flight[8],
#                 f"₹{flight[4]}",
#                 str(flight[5]),
#                 str(flight[6])
#             )

#         console.print(table)

#         # ✅ Select flight
#         choice = int(input("\nSelect flight (index): ")) - 1

#         if choice < 0 or choice >= len(flights):
#             print("❌ Invalid selection")
#             return False

#         selected = flights[choice]

#         flight_id = selected[0]
#         flight_name = selected[1]
#         base_price = selected[4]
#         eco_available = selected[5]
#         bus_available = selected[6]
#         carrier_id = selected[7]
#         carrier_name = selected[8]
#         silver_discount = selected[9]
#         gold_discount = selected[10]

#         # ✅ Select seat type
#         seat_type = input("Select seat type (economy/business): ").strip().lower()

#         if seat_type == "economy":
#             if eco_available < no_of_passengers:
#                 print("❌ Not enough economy seats available.")
#                 return False
#         elif seat_type == "business":
#             if bus_available < no_of_passengers:
#                 print("❌ Not enough business seats available.")
#                 return False
#         else:
#             print("❌ Invalid seat type.")
#             return False

#         # ✅ Journey date in dd-mm-yyyy
#         journey_date = input("Enter journey date (dd-mm-yyyy): ").strip()

#         try:
#             datetime.strptime(journey_date, "%d-%m-%Y")
#         except ValueError:
#             print("❌ Invalid date format. Use dd-mm-yyyy.")
#             return False

#         # ✅ Get user tier
#         cursor.execute("""
#             SELECT user_tier FROM Users
#             WHERE user_name = ?
#         """, (state.user_name,))
#         user = cursor.fetchone()

#         user_tier = user[0] if user else "regular"

#         discount = 0
#         if user_tier.lower() == "silver":
#             discount = silver_discount
#         elif user_tier.lower() == "gold":
#             discount = gold_discount

#         discounted_price = base_price * (1 - discount / 100)
#         total_price = discounted_price * no_of_passengers

#         # ✅ Booking summary
#         print("\n" + "=" * 50)
#         print("BOOKING SUMMARY")
#         print("=" * 50)
#         print(f"Flight: {flight_name} ({carrier_name})")
#         print(f"Route: {source} → {destination}")
#         print(f"Seat Type: {seat_type.capitalize()}")
#         print(f"Journey Date: {journey_date}")
#         print(f"Passengers: {no_of_passengers}")
#         print(f"User Tier: {user_tier.upper()}")
#         print(f"Total Amount: ₹{total_price:.2f}")
#         print("=" * 50)

#         confirm = input("Confirm booking? (y/n): ").strip().lower()

#         if confirm != "y":
#             print("❌ Booking cancelled.")
#             return False

#         # ✅ Reduce available seats
#         if seat_type == "economy":
#             cursor.execute("""
#                 UPDATE Flights
#                 SET economy_available_seats = economy_available_seats - ?
#                 WHERE flight_id = ?
#             """, (no_of_passengers, flight_id))
#         else:
#             cursor.execute("""
#                 UPDATE Flights
#                 SET business_available_seats = business_available_seats - ?
#                 WHERE flight_id = ?
#             """, (no_of_passengers, flight_id))

#         # ✅ Insert booking
#         booking_date = datetime.now().strftime("%d-%m-%Y")

#         cursor.execute("""
#             INSERT INTO Bookings (
#                 user_name,
#                 flight_id,
#                 carrier_id,
#                 source,
#                 destination,
#                 journey_date,
#                 no_of_passengers,
#                 seat_type,
#                 base_price,
#                 discount_percent,
#                 total_price,
#                 booking_date,
#                 status
#             )
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             state.user_name,
#             flight_id,
#             carrier_id,
#             source,
#             destination,
#             journey_date,
#             no_of_passengers,
#             seat_type,
#             base_price,
#             discount,
#             total_price,
#             booking_date,
#             "confirmed"
#         ))

#         conn.commit()

#         print("\n🎉 BOOKING CONFIRMED 🎉")
#         print(f"Booking ID: {cursor.lastrowid}")
#         print(f"Booking Date: {booking_date}")
#         print(f"Total Paid: ₹{total_price:.2f}\n")

#         return True

#     except Exception as e:
#         conn.rollback()
#         print(f"❌ Error: {e}")
#         return False

#     finally:
#         conn.close()


# # Helper function
# def initiate_booking():
#     print("\n" + "=" * 50)
#     print("FLIGHT BOOKING")
#     print("=" * 50)

#     source = input("Enter departure city: ").strip()
#     destination = input("Enter destination city: ").strip()
#     no_of_passengers = int(input("Enter number of passengers: "))

#     if no_of_passengers <= 0:
#         print("❌ Invalid passenger count.")
#         return

#     book_ticket(source, destination, no_of_passengers)
