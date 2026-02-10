import sqlite3 as sql
from rich.console import Console
from rich.table import Table

conn = sql.connect("airline.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("DROP TABLE IF EXISTS Carriers")
cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute("DROP TABLE IF EXISTS Flights")
cursor.execute("DROP TABLE IF EXISTS Bookings")

cursor.execute("""
CREATE TABLE Flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_name TEXT NOT NULL,
    start_loc TEXT NOT NULL,
    end_loc TEXT NOT NULL,
    base_price INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Users ( 
    user_name TEXT PRIMARY KEY,
    user_pass TEXT NOT NULL,
    dob TEXT NOT NULL,
    email_Id TEXT NOT NULL,
    phone INTEGER NOT NULL,
    address1 TEXT NOT NULL,
    address2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    zipcode INTEGER NOT NULL,
    user_tier TEXT NOT NULL DEFAULT 'regular'
)
""")

cursor.execute("""
CREATE TABLE Carriers ( 
    carrier_id INTEGER PRIMARY KEY,
    carrier_name TEXT NOT NULL,
    refund_before_2days_of_travel INTEGER NOT NULL,
    refund_before_10days_of_travel INTEGER NOT NULL,
    refund_before_20days_of_travel INTEGER NOT NULL,
    silver_user_discount INTEGER NOT NULL,
    gold_user_discount INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
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
            ("Indigo", "Delhi", "Mumbai"),
            ("VistaAir", "Mumbai", "Delhi"),
            ("AirIndia", "Chennai", "Bangalore"),
            ("SpiceJet", "Bangalore", "Chennai"),
            ("Emir", "Hyderabad", "Delhi"),
            ("Indigo", "Delhi", "Hyderabad"),
            ("Indigo", "Kolkata", "Mumbai"),
            ("AirVista", "Mumbai", "Kolkata"),
            ("AirIndia", "Pune", "Delhi"),
            ("SpiceJet", "Delhi", "Pune"),
        ]

        cur.executemany("""
            INSERT INTO Flights (flight_name, start_loc, end_loc)
            VALUES (?, ?, ?)
        """, flights)

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
