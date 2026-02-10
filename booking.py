import sqlite3 as sql
from rich.console import Console
from rich.table import Table
from datetime import datetime
from state import state

def book_ticket(source, destination, date_from, date_to, no_of_passengers):
    conn = sql.connect('airline.db')
    cursor = conn.cursor()
    console = Console()
    
    try:
        # Step 1: Search for available flights
        print(f"\n🔍 Searching flights from {source} to {destination}...\n")
        
        cursor.execute("""
            SELECT f.flight_id, f.flight_name, f.start_loc, f.end_loc,
                   c.carrier_Id, c.carrier_name, 
                   c.silver_user_discount, c.gold_user_discount
            FROM Flights f
            JOIN Carriers c ON f.flight_id = c.flight_id
            WHERE LOWER(f.start_loc) = LOWER(?) 
            AND LOWER(f.end_loc) = LOWER(?)
        """, (source, destination))
        
        available_flights = cursor.fetchall()
        
        if not available_flights:
            print(f"❌ No flights available from {source} to {destination}")
            return False
        
        # Step 2: Display available flights
        table = Table(title=f"Available Flights: {source} → {destination}")
        table.add_column("Index", style="yellow")
        table.add_column("Flight ID", style="cyan")
        table.add_column("Flight Name", style="green")
        table.add_column("Carrier", style="magenta")
        table.add_column("Route", style="blue")
        
        for idx, flight in enumerate(available_flights, 1):
            route = f"{flight[2]} → {flight[3]}"
            table.add_row(
                str(idx),
                str(flight[0]),
                flight[1],
                flight[5],
                route
            )
        
        console.print(table)
        
        # Step 3: Select flight
        flight_choice = int(input("\nSelect flight (enter index number): ")) - 1
        
        if flight_choice < 0 or flight_choice >= len(available_flights):
            print("❌ Invalid selection")
            return False
        
        selected_flight = available_flights[flight_choice]
        flight_id = selected_flight[0]
        carrier_id = selected_flight[4]
        carrier_name = selected_flight[5]
        silver_discount = selected_flight[6]
        gold_discount = selected_flight[7]
        
        # Step 4: Get base price
        base_price = float(input("\nEnter base ticket price per passenger: ₹"))
        
        # Step 5: Get user tier and apply discount
        cursor.execute(
            "SELECT user_tier FROM Users WHERE user_name = ?",
            (state.user_name,)
        )
        user_data = cursor.fetchone()
        user_tier = user_data[0] if user_data else "regular"
        
        discount = 0
        if user_tier.lower() == "silver":
            discount = silver_discount
        elif user_tier.lower() == "gold":
            discount = gold_discount
        
        # Calculate total price
        discounted_price = base_price * (1 - discount / 100)
        total_price = discounted_price * no_of_passengers
        
        # Step 6: Display booking summary
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
        
        # Step 7: Confirm booking
        confirm = input("\nConfirm booking? (y/n): ")
        
        if confirm.lower() != 'y':
            print("❌ Booking cancelled")
            return False
        
        # Step 8: Insert booking into database
        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            'confirmed'
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
    
    source = input("Enter departure city: ").strip()
    destination = input("Enter destination city: ").strip()
    date_from = input("Enter departure date (YYYY-MM-DD): ").strip()
    
    trip_type = input("One-way or Round-trip? (o/r): ").strip().lower()
    date_to = None
    if trip_type == 'r':
        date_to = input("Enter return date (YYYY-MM-DD): ").strip()
    
    no_of_passengers = int(input("Enter number of passengers: "))
    
    if no_of_passengers <= 0:
        print("❌ Invalid number of passengers")
        return
    
    # Call the booking function
    book_ticket(source, destination, date_from, date_to, no_of_passengers)