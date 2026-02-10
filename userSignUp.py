import sqlite3 as sql
import bcrypt
from datetime import date

DB_NAME = "airline.db"

def get_connection():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor


# SIGNUP FIELDS ALONG WITH VALIDATION 


def create_username(cursor):
    while True:
        username = input("Create username (min 5 chars) ➜ ").strip()
        if len(username) < 5:
            print("Username must be at least 5 characters.")
            continue

        cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE user_name = ?",
            (username,)
        )
        if cursor.fetchone()[0] > 0:
            print("Username already exists.")
            continue

        return username


def create_password():
    while True:
        password = input("Create password (8–14 chars) ➜ ").replace(" ", "")
        if not 8 <= len(password) <= 14:
            print("Password length must be 8–14 characters.")
            continue

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def get_email():
    while True:
        email = input("Enter Gmail ID ➜ ").strip()
        if email.endswith("@gmail.com") and len(email) > 10:
            return email
        print("Invalid Gmail address.")


def get_phone():
    while True:
        phone = input("Enter phone number ➜ ").strip()
        if phone.isdigit() and len(phone) == 10 and phone[0] in "6789":
            return int(phone)
        print("Invalid Indian phone number.")


# def get_non_empty(prompt, min_len=2):
#     while True:
#         value = input(prompt).strip()
#         if len(value) >= min_len:
#             return value
#         print(f"Must be at least {min_len} characters.")


def get_zipcode():
    while True:
        z = input("Enter Zip Code ➜ ").strip()
        if z.isdigit() and 4 <= len(z) <= 10:
            return int(z)
        print("Invalid Zip Code.")


def get_dob():
    while True:
        dob = input("DOB (dd/mm/yyyy) ➜ ")
        if len(dob) == 10 and dob[2] == "/" and dob[5] == "/":
            d, m, y = dob[:2], dob[3:5], dob[6:]
            if d.isdigit() and m.isdigit() and y.isdigit():
                return dob
        print("Invalid DOB format.")

def get_address1():
    while True:
        address1 = input("Enter Address Line 1 ➜ ").strip()
        if address1:
            return address1
        print("Address Line 1 cannot be empty.")

def get_address2():
    address2 = input("Enter Address Line 2 (optional) ➜ ").strip()
    return address2

def get_city():
    while True:
        city = input("Enter City ➜ ").strip()
        if city:
            return city
        print("City cannot be empty.")

def get_state():
    while True:
        state = input("Enter State ➜ ").strip()
        if state:
            return state
        print("State cannot be empty.")

def get_country():
    while True:
        country = input("Enter Country ➜ ").strip()
        if country:
            return country
        print("Country cannot be empty.")



# ==================================================
# USER SIGNUP
# ==================================================

def usersignup():
    conn, cursor = get_connection()

    print("\n=== USER REGISTRATION ===\n")

    username = create_username(cursor)
    password = create_password()
    dob = get_dob()
    
    email = get_email()
    phone=get_phone()
    a1=get_address1()
    a2=get_address2()
    city=get_city()
    state=get_state()
    country=get_country()
    zipcode=get_zipcode()

    cursor.execute(
        "INSERT INTO Users(user_name, user_pass, dob, email_Id,phone,address1,address2,city,state,country,zipcode) VALUES (?, ?, ?, ?,?,?,?, ?, ?, ?,?)",
        (username, password, dob, email,phone,a1,a2,city,state,country,zipcode)
    )

    print("\nBasic account created successfully ✔\n")


    conn.commit()
    conn.close()

    print("\nUser registration completed 🎉\n")
    


    # update_user_profile(username, cursor, commit=False)
# ==================================================
# UPDATE / EDIT USER PROFILE
# ==================================================

# def update_user_profile(username, cursor=None, commit=True):
#     external_conn = False

#     if cursor is None:
#         conn, cursor = get_connection()
#         ensure_user_columns(cursor)
#         external_conn = True

#     print("\n=== USER PROFILE DETAILS ===\n")

#     phone = get_phone()
#     address1 = get_non_empty("Address Line 1 ➜ ")
#     address2 = input("Address Line 2 (optional) ➜ ").strip()
#     city = get_non_empty("City ➜ ")
#     state = get_non_empty("State ➜ ")
#     country = get_non_empty("Country ➜ ")
#     zipcode = get_zipcode()
#     dob = get_dob()

#     cursor.execute("""
#         UPDATE Users
#         SET phone = ?, address1 = ?, address2 = ?, city = ?, state = ?,
#             country = ?, zipcode = ?, dob = ?
#         WHERE user_name = ?
#     """, (phone, address1, address2, city, state, country, zipcode, dob, username))

#     if external_conn and commit:
#         conn.commit()
#         conn.close()

#     print("Profile details saved ✔")
