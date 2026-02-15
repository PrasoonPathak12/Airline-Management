import sqlite3 as sql
from rich.console import Console
from rich.table import Table

conn = sql.connect("airline.db")
cursor = conn.cursor()

# cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("DROP TABLE IF EXISTS Carriers")
cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute("DROP TABLE IF EXISTS Flights")
cursor.execute("DROP TABLE IF EXISTS Bookings")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_name TEXT NOT NULL,
    start_loc TEXT NOT NULL,
    end_loc TEXT NOT NULL,
    base_price INTEGER NOT NULL,
    economy_no_of_seats INTEGER NOT NULL,
    business_no_of_seats INTEGER NOT NULL,
    economy_available_seats INTEGER NOT NULL,
    business_available_seats INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users ( 
    user_name TEXT PRIMARY KEY,
    user_pass TEXT NOT NULL,
    dob TEXT NOT NULL,
    email_Id TEXT NOT NULL,
    phone INTEGER NOT NULL,
    address1 TEXT NOT NULL,
    address2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT DEFAULT 'INDIA',
    zipcode INTEGER NOT NULL,
    user_tier TEXT NOT NULL DEFAULT 'regular'
)
""")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Carriers ( 
#     carrier_id INTEGER PRIMARY KEY,
#     carrier_name TEXT NOT NULL,
#     refund_before_2days_of_travel INTEGER NOT NULL,
#     refund_before_10days_of_travel INTEGER NOT NULL,
#     refund_before_20days_of_travel INTEGER NOT NULL,
#     silver_user_discount INTEGER NOT NULL,
#     gold_user_discount INTEGER NOT NULL,
#     flight_id INTEGER NOT NULL,
#     start_time TEXT NOT NULL,
#     end_time TEXT NOT NULL,
#     FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
# )
# """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Carriers ( 
    carrier_id INTEGER PRIMARY KEY,
    carrier_name TEXT NOT NULL,
    refund_before_2days_of_travel INTEGER NOT NULL,
    refund_before_10days_of_travel INTEGER NOT NULL,
    refund_before_20days_of_travel INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    date_of_journey TEXT NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    flight_id INTEGER NOT NULL,
    carrier_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_date TEXT NOT NULL,
    return_date TEXT,
    no_of_passengers INTEGER NOT NULL,
    base_price REAL NOT NULL,
    discount_percent INTEGER DEFAULT 0,
    total_price REAL NOT NULL,
    booking_date TEXT NOT NULL,
    status TEXT DEFAULT 'confirmed',
    seat_type TEXT NOT NULL,
    FOREIGN KEY (user_name) REFERENCES Users(user_name),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
    FOREIGN KEY (carrier_id) REFERENCES Carriers(Carrier_Id)
)
""")

# ================== SEED DATA ==================
def seed_default_flights(cur):
    cur.execute("SELECT COUNT(*) FROM Flights")
    count = cur.fetchone()[0]

    if count==0:
        flights = [
            ("Indigo", "Delhi", "Mumbai",2000,50,50,50,50),
            ("VistaAir", "Mumbai", "Delhi",3000,50,50,50,50),
            ("AirIndia", "Chennai", "Bangalore",4000,50,50,50,50),
            ("SpiceJet", "Bangalore", "Chennai",1888,50,50,50,50),
            ("Emir", "Hyderabad", "Delhi",3000,50,50,50,50),
            ("Indigo", "Delhi", "Hyderabad",2000,50,50,50,50),
            ("Indigo", "Kolkata", "Mumbai",2000,50,50,50,50),
            ("AirVista", "Mumbai", "Kolkata",5000,50,50,50,50),
            ("AirIndia", "Pune", "Delhi",4000,50,50,50,50),
            ("SpiceJet", "Delhi", "Pune",5000,50,50,50,50),
        ]

        cur.executemany("""
                INSERT INTO Flights (flight_name, start_loc, end_loc,base_price,economy_no_of_seats,business_no_of_seats,
                economy_available_seats,business_available_seats)
                VALUES (?, ?, ?,?,?,?,?,?)
            """, flights)

        carriers = [
        # flight_id 1 (Delhi → Mumbai)
        (11,"Indigo Express", 40, 60, 80, 1, "06:00", "08:00","19-02-2026"),
        (12,"Vista Premium", 50, 70, 90, 1, "18:00", "20:00","28-02-2026"),

        # flight_id 2 (Mumbai → Delhi)
        (22,"AirIndia Flex", 30, 60, 85, 2, "07:00", "09:30","09-03-2026"),
        (23,"SkyJet", 45, 65, 88, 2, "19:00", "21:00","19-02-2026"),

        # flight_id 3 (Chennai → Bangalore)
        (33,"SouthAir", 35, 55, 75, 3, "09:00", "10:00","18-02-2026"),
        (34,"QuickFly", 40, 60, 80, 3, "17:00", "18:00","19-02-2026"),

        # flight_id 4 (Bangalore → Chennai)
        (41,"FlyFast", 42, 62, 82, 4, "08:30", "09:30","22-04-2026"),
        (42,"AirConnect", 38, 58, 78, 4, "16:00", "17:00","29-04-2026"),

        # flight_id 5 (Hyderabad → Delhi)
        (51,"DeccanAir", 33, 63, 83, 5, "05:00", "07:30","04-03-2026"),
        (52,"CapitalWings", 48, 68, 88, 5, "20:00", "22:30","14-03-2026"),

        # flight_id 6 (Delhi → Hyderabad)
        (61,"MetroFly", 37, 57, 77, 6, "06:30", "08:30","15-05-2026"),
        (62,"JetSky", 44, 64, 84, 6, "18:30", "20:30","23-05-2026"),

        # flight_id 7 (Kolkata → Mumbai)
        (71,"EastWest Air", 36, 66, 86, 7, "07:45", "10:15","26-02-2026"),
        (72,"BengalFly", 49, 69, 89, 7, "19:15", "21:45","28-09-2026"),

        # flight_id 8 (Mumbai → Kolkata)
        (81,"WesternAir", 39, 59, 79, 8, "08:00", "10:30","28-08-2026"),
        (82,"CityWings", 46, 76, 96, 8, "17:30", "20:00","14-12-2026"),

        # flight_id 9 (Pune → Delhi)
        (91,"PuneExpress", 41, 61, 81, 9, "06:15", "08:45","17-07-2026"),
        (92,"NorthBound", 47, 67, 87, 9, "19:45", "22:15","11-06-2026"),

        # flight_id 10 (Delhi → Pune)
        (101,"CapitalAir", 34, 54, 74, 10, "07:00", "09:30","13-03-2026"),
        (102,"SwiftJet", 50, 70, 90, 10, "18:00", "20:30","14-03-2026"),
    ]

    cur.executemany("""
        INSERT INTO Carriers (
            carrier_id,
            carrier_name,
            refund_before_2days_of_travel,
            refund_before_10days_of_travel,
            refund_before_20days_of_travel,
            flight_id,
            start_time,
            end_time,
            date_of_journey
        )
        VALUES (?,?, ?, ?, ?, ?, ?, ?,?)
    """, carriers)


seed_default_flights(cursor)

cursor.execute("SELECT * FROM Flights")
rows = cursor.fetchall()

table = Table(title="Flights Data")

columns = [desc[0] for desc in cursor.description]
for col in columns:
    table.add_column(col, style="cyan")

for row in rows:
    table.add_row(*map(str, row))

console = Console()
console.print(table)

conn.commit()
conn.close()
