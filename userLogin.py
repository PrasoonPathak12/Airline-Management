import sqlite3 as sql
import bcrypt
from User_Dashboard import userDashboard
from state import state

def user_login():
    conn = sql.connect('airline.db')
    cursor = conn.cursor()

    user_name = input("Enter user name: ")
    user_pass = input("Enter account password: ")

    cursor.execute(
        "SELECT user_pass FROM Users WHERE user_name = ?",
        (user_name,)
    )

    result = cursor.fetchone()

    if result is None:
        print("No such user exists...")
        conn.close()
        return False
    else:
        db_password = result[0]
        if isinstance(db_password, str):
            db_password = db_password.encode('utf-8')

        if bcrypt.checkpw(user_pass.encode('utf-8'), db_password):
            print(f"Welcome {user_name}")
            state.user_name = user_name
            userDashboard()
            conn.close()
            return True
        else:
            print("Incorrect password")

    conn.close()
    return False
