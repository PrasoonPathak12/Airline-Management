import sqlite3 as sql
import bcrypt
from datetime import date
import pwinput
from state import state
import sys

DB_NAME = "airline.db"

def get_connection():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor


# SIGNUP FIELDS ALONG WITH VALIDATION 


def create_username(cursor):
    while True:
        try:
            username = input("Create username (min 5 chars) ➜ ").strip()
            if len(username) < 5:
                print("Username must be at least 5 characters.")
                continue
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the program...")

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
        try:    
            password = pwinput.pwinput(prompt="Enter user password: ", mask='*').replace(" ", "")
            if not 8 <= len(password) <= 14:
                print("Password length must be 8–14 characters.")
                continue
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")   

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def get_email():
    while True:
        try:
            email = input("Enter Gmail ID ➜ ").strip()
            if email.endswith("@gmail.com") and len(email) > 10:
                return email
            print("Invalid Gmail address.")
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")


def get_phone():
    while True:
        try:    
            phone = input("Enter phone number ➜ ").strip()
            if phone.isdigit() and len(phone) == 10 and phone[0] in "6789":
                return int(phone)
            print("Invalid Indian phone number.")

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")


# def get_non_empty(prompt, min_len=2):
#     while True:
#         value = input(prompt).strip()
#         if len(value) >= min_len:
#             return value
#         print(f"Must be at least {min_len} characters.")


def get_zipcode():
    while True:
        try:
            value = input("Enter zip code : ")
            if(len(value)==6 and value.isdigit() and int(value[0])>=1):
                # print("Only valid code...")    
                return int(value)
            else:
                print("🛑🛑Enter valid zip values starting with 1-9 and length of 6...")
                # continue

        except ValueError:
            print("❌ Invalid input. Must be a number.")
            return
        except KeyboardInterrupt:
                print("⚠️⚠️⚠️Exiting program....")
                sys.exit()


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    # while True:
    #     dob = input("DOB (dd/mm/yyyy) ➜ ")
    #     if len(dob) == 10 and dob[2] == "/" and dob[5] == "/":
    #         d, m, y = dob[:2], dob[3:5], dob[6:]
    #         if d.isdigit() and m.isdigit() and y.isdigit():
    #             return dob
    #     print("Invalid DOB format.")


    

def get_dob():
    while True:
        try:
            dob=input("Enter your date of birth in dd/mm/yyyy format only ---> ")
            
            if len(dob) != 10 or dob[2] != '/' or dob[5] != '/':
                print("Date must be in dd/mm/yyyy format\n\n")
                continue

            day_str, month_str, year_str = dob[0:2], dob[3:5], dob[6:10]

            if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
                print("Date, month, and year must be numeric")
                continue

            day, month, year = int(day_str), int(month_str), int(year_str)

            if year < 1908 or year > 2008:
                print("Either you are underage or entering wrong year value")
                continue
            if month < 1 or month > 12:
                print("Month must be between 1 and 12")
                continue

            days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30,
                        31, 31, 30, 31, 30, 31]

            if day < 1 or day > days_in_month[month - 1]:
                print(f"Invalid day for month {month}: must be 1-{days_in_month[month-1]}")
                continue
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")

        return dob
    

def get_address1():
    while True:
        try:
            address1 = input("Enter Address Line 1 ➜ ").strip()
            if address1:
                return address1
            print("Address Line 1 cannot be empty.")
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")

def get_address2():
    while True:
        try:
            address2 = input("Enter Address Line 2 (optional) ➜ ").strip()
            return address2
        except Exception as e:
                print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")

def get_city():
    while True:
        try:
            city = input("Enter City ➜ ").strip()
            if city:
                return city
            print("City cannot be empty.")
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")

# def get_user_tier():
#     while True:
#         try:
#             tier = input("Enter City ➜ ").strip()
#             if city:
#                 return city
#             print("City cannot be empty.")
#         except Exception as e:
#             print(e)
#         except KeyboardInterrupt:
#             print("⚠️⚠️⚠️Exiting the application....")

def get_state():
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
    while True:
        try:
            State = input("Enter State ➜ ").strip()
            if State not in states:
                print("❓❓Enter valid Indian state...")
                continue
            return State
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the application....")

# def get_country():
#     while True:
#         country = input("Enter Country ➜ ").strip()
#         if country:
#             return country
#         print("Country cannot be empty.")

def get_userTier():
    while True:
        try:   
            print("Select tier from below: \n\n1-->Regular(No discount) ,,, 2 --> Silver(5% discount) ,,, 3 --> Gold(7% discount))\n\n")    
            user_tier=input("Type your option: ")
            if user_tier.strip().lower() not in ("regular","silver","gold"):
                print("Select from available options only...")
                continue
            
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("⚠️⚠️⚠️Exiting the program....")
        return user_tier




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
    State=get_state()
    # country=get_country()
    zipcode=get_zipcode()
    user_tier=get_userTier()

    cursor.execute(
        "INSERT INTO Users(user_name, user_pass, dob, email_Id,phone,address1,address2,city,state,zipcode,user_tier) VALUES (?, ?, ?, ?,?,?, ?, ?, ?,?,?)",
        (username, password, dob, email,phone,a1,a2,city,State,zipcode,user_tier)
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
