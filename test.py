import sqlite3 as sql
from rich.console import Console
from rich.table import Table

conn = sql.connect("airline.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM Flights")
rows = cursor.fetchall()

console=Console()

# print("Carriers: ", carriers_before)

# cursor.execute("SELECT * FROM Flights")
# carriers_after = cursor.fetchall()
# print("Flights:", carriers_after)

# cursor.execute("""SELECT f.flight_id, f.flight_name, f.start_loc, f.end_loc,
#                    c.carrier_Id, c.carrier_name, 
#                    c.silver_user_discount, c.gold_user_discount
#             FROM Flights f
#             JOIN Carriers c ON f.flight_id = c.flight_id
#             WHERE LOWER(f.start_loc) = LOWER(?) 
#             AND LOWER(f.end_loc) = LOWER(?)""",("delhi","mumbai"))
# us = cursor.fetchall()
# print("Use: ", us)

table = Table(title="Flights")
columns = [desc[0] for desc in cursor.description] 

for col in columns:
    table.add_column(col,style="cyan")

for row in rows:
    table.add_row(*map(str,row))

# for col in columns:
#     table.add_column(col, style="cyan")

# for u in us:
#     table.add_row(*map(str, u))

# console = Console()
console.print(table)