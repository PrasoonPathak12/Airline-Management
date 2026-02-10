import sqlite3 as sql
from rich.console import Console
from rich.table import Table

conn = sql.connect("airline.db")
cursor = conn.cursor()

# cursor.execute("SELECT * FROM Carriers")
# carriers_before = cursor.fetchall()
# print("Carriers: ", carriers_before)

# cursor.execute("SELECT * FROM Flights")
# carriers_after = cursor.fetchall()
# print("Flights:", carriers_after)

cursor.execute("SELECT * FROM Bookings")
bookings = cursor.fetchall()
print("Bookings: ", bookings)

table = Table(title="Bookings")

columns = [desc[0] for desc in cursor.description]
for col in columns:
    table.add_column(col, style="cyan")

for booking in bookings:
    table.add_row(*map(str, booking))

console = Console()
console.print(table)