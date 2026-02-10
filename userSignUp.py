import sqlite3 as sql
import bcrypt
from datetime import date
conn=sql.connect('airline.db')
cursor=conn.cursor()


def usersignup():
    def createUserName():
        while True:
            username=input("Create your username ---> ")
            if not username.strip():
                print("User Name cannot be empty....")
                continue
            if(len(username) < 5):
                print("Username must at least be of length 5...")
            cursor.execute('SELECT COUNT(*) FROM Users WHERE user_name=?',(username,))
            userN = cursor.fetchone()[0]
            if(userN > 0):
                print("Please select a different user name....")
                print("==============================")
            # createUserName()
            else:
                print(f"Username '{username}' generated successfully...")
                return username

    def createPassword():
        while True:

            userpass=input("Create user password(min 8 characters in length and maximum 14)--->")
            clean_userpass=userpass.replace(" ","")
            if(len(clean_userpass)<8 or len(clean_userpass)>14):
                print("Password must be between 8 to 14 characters in length")
                continue
            else:
                hash_password=bcrypt.hashpw(clean_userpass.encode('utf-8'),bcrypt.gensalt())
                print("Password created successfully")
                return hash_password

    username=createUserName()
    userpass=createPassword()

    ## DOB VERIFICATION ##

    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def date_of_birth():

        while True:
            dob=input("Enter your date of birth in dd/mm/yyyy format only ---> ")

            if len(dob) != 10 or dob[2] != '/' or dob[5] != '/':
                print("Date must be in dd/mm/yyyy format\n\n")
                continue

            day_str, month_str, year_str = dob[0:2], dob[3:5], dob[6:10]

            if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
                print("Date, month, and year must be numeric")
                continue

            day, month, year = int(day_str), int(month_str), int(year_str)

            if year < 1900 or year > 2026:
                print("Year must be between 1900 and 2100")
                continue
            if month < 1 or month > 12:
                print("Month must be between 1 and 12")
                continue

            days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30,
                     31, 31, 30, 31, 30, 31]

            if day < 1 or day > days_in_month[month - 1]:
                print(f"Invalid day for month {month}: must be 1-{days_in_month[month-1]}")
                continue

            return dob

    dob=date_of_birth()
    year=int(dob[6:10])
    month=int(dob[3:5])
    day=int(dob[0:2])
    today=date.today()
    age = today.year - year - (
        (month,day)>(today.month,today.day)
    )

    def email_Of_User():
        while True:
            email=input("Enter your email Id ---> ")
            if(email[-10:]!="@gmail.com"):
                print("Enter google domain email id...")
                continue
            clean_email=email.replace(" ","")

            if(len(clean_email)<11):
                print("Provide proper email...")
                continue
            return email

    email = email_Of_User()

   

    # ============================
# ADDITIONS: extra input & edit/save profile
# ============================


    def phone_of_user():
        while True:
            raw = input("Enter your phone number (digits only) ---> ")
            phone = raw.strip().replace(" ", "")
            if not phone.isdigit():
                print("Phone must be numeric.")
                continue
        # Common mobile length checks (customize if needed)
            if len(phone)!=10:
                print("Phone length must be of 10 digits in length.")
                continue
            if phone[0] not in ('6','7','8','9'):
                print("Enter Indian phone numbers only")
                continue
            return int(phone)

    def address1_of_user():
        while True:
            a1 = input("Enter Address Line 1 ---> ").strip()
            if not a1:
                print("Address Line 1 cannot be empty.")
                continue
            return a1

    def address2_of_user():
        # Optional; allow empty, but trim spaces
        a2 = input("Enter Address Line 2 (optional) ---> ").strip()
        return a2

    def city_of_user():
        while True:
            city = input("Enter City ---> ").strip()
            if len(city) < 2:
                print("City must be at least 2 characters.")
                continue
            return city

    def state_of_user():
        while True:
            state = input("Enter State/Province ---> ").strip()
            if len(state) < 2:
                print("State must be at least 2 characters.")
                continue
            return state

    def country_of_user():
        while True:
            country = input("Enter Country ---> ").strip()
            if len(country) < 2:
                print("Country must be at least 2 characters.")
                continue
            return country

    def zipcode_of_user():
        while True:
            raw = input("Enter Zip/Postal Code (digits only) ---> ")
            z = raw.strip().replace(" ", "")
            if not z.isdigit():
                print("Zip/Postal Code must be numeric.")
                continue
            # Typical ranges (customize as per country; India=6, US=5/9, etc.)
            if len(z) < 4 or len(z) > 10:
                print("Zip/Postal Code length must be between 4 and 10 digits.")
                continue
            return int(z)

    # If you also want to store DOB as a Date-like text (you already collected dob):
    # We'll reuse your dd/mm/yyyy as TEXT in DB so you keep exact date.
    def ensure_user_columns(cursor):
        """
        Safely add columns to Users table if missing.
        Uses try/except around ALTER TABLE (valid for SQLite).
        """
        # Column types chosen to match intent. SQLite is dynamic-typed but we'll keep it clean.
        alter_statements = [
            "ALTER TABLE Users ADD COLUMN phone INTEGER",
            "ALTER TABLE Users ADD COLUMN address1 TEXT",
            "ALTER TABLE Users ADD COLUMN address2 TEXT",
            "ALTER TABLE Users ADD COLUMN city TEXT",
            "ALTER TABLE Users ADD COLUMN state TEXT",
            "ALTER TABLE Users ADD COLUMN country TEXT",
            "ALTER TABLE Users ADD COLUMN zipcode INTEGER",
            "ALTER TABLE Users ADD COLUMN dob TEXT"  # store dd/mm/yyyy as entered
        ]
        for stmt in alter_statements:
            try:
                cursor.execute(stmt)
            except sql.OperationalError:
                # Column probably already exists; ignore
                pass

    def save_additional_profile_fields(cursor, username, phone, address1, address2, city, state, country, zipcode, dob_text):
        """
        Update the Users row for the given username with the new fields.
        """
        # Ensure columns exist before updating
        ensure_user_columns(cursor)

        cursor.execute("""
            UPDATE Users
            SET phone = ?,
                address1 = ?,
                address2 = ?,
                city = ?,
                state = ?,
                country = ?,
                zipcode = ?,
                dob = ?
            WHERE user_name = ?
        """, (phone, address1, address2, city, state, country, zipcode, dob_text, username))

    # --- Prompt and save additional fields as part of signup flow ---

    # Collect extra profile data
    phone = phone_of_user()
    addr1 = address1_of_user()
    addr2 = address2_of_user()
    city = city_of_user()
    state = state_of_user()
    country = country_of_user()
    zipc = zipcode_of_user()

    # Save them along with DOB you already captured as `dob` (dd/mm/yyyy)
    save_additional_profile_fields(cursor,username, phone, addr1, addr2, city, state, country, zipc, dob)

    print("Additional profile details saved successfully.")


    # ============================
    # OPTIONAL: Edit/Update profile later
    # ============================
    def edit_profile(existing_username):
        """
        Allows user to edit and save profile fields later.
        Hit ENTER to keep existing values.
        """
        # Reuse same connection or open a new one if you call this outside usersignup()
        # Using current `cursor` and `conn` here—if calling standalone, re-open DB.

        ensure_user_columns(cursor)

        # Fetch current values
        cursor.execute("""
            SELECT phone, address1, address2, city, state, country, zipcode, dob
            FROM Users
            WHERE user_name = ?
        """, (existing_username,))
        row = cursor.fetchone()

        if not row:
            print("User not found.")
            return

        curr_phone, curr_a1, curr_a2, curr_city, curr_state, curr_country, curr_zip, curr_dob = row

        # Helper: prompt with default
        def prompt_default(prompt_text, current_val):
            shown = "" if current_val is None else str(current_val)
            typed = input(f"{prompt_text} [{shown}] ---> ").strip()
            return shown if typed == "" else typed

        # Phone (validate if changed)
        new_phone_in = prompt_default("Phone (digits only)", curr_phone)
        if str(new_phone_in) != str(curr_phone):
            while True:
                p = str(new_phone_in).replace(" ", "")
                if p.isdigit() and 7 <= len(p) <= 15:
                    curr_phone = int(p)
                    break
                print("Invalid phone; must be digits 7-15 in length.")
                new_phone_in = input("Re-enter Phone ---> ").strip()

        # Address1
        new_a1 = prompt_default("Address Line 1", curr_a1)
        curr_a1 = new_a1 if new_a1 else curr_a1

        # Address2
        new_a2 = prompt_default("Address Line 2 (optional)", curr_a2)
        curr_a2 = new_a2  # can be empty

        # City
        new_city = prompt_default("City", curr_city)
        curr_city = new_city if new_city else curr_city

        # State
        new_state = prompt_default("State/Province", curr_state)
        curr_state = new_state if new_state else curr_state

        # Country
        new_country = prompt_default("Country", curr_country)
        curr_country = new_country if new_country else curr_country

        # ZipCode (validate if changed)
        new_zip_in = prompt_default("Zip/Postal Code (digits only)", curr_zip)
        if str(new_zip_in) != str(curr_zip):
            while True:
                z = str(new_zip_in).replace(" ", "")
                if z.isdigit() and 4 <= len(z) <= 10:
                    curr_zip = int(z)
                    break
                print("Invalid zip/postal code; must be digits with length 4-10.")
                new_zip_in = input("Re-enter Zip/Postal Code ---> ").strip()

        # DOB (keep your dd/mm/yyyy format)
        new_dob = prompt_default("DOB (dd/mm/yyyy)", curr_dob)
        if new_dob != curr_dob:
            # quick format check to be consistent with your earlier logic
            if len(new_dob) == 10 and new_dob[2] == '/' and new_dob[5] == '/':
                d, m, y = new_dob[0:2], new_dob[3:5], new_dob[6:10]
                if d.isdigit() and m.isdigit() and y.isdigit():
                    curr_dob = new_dob
                else:
                    print("Invalid DOB; keeping previous value.")
            else:
                print("Invalid DOB format; keeping previous value.")

        # Persist updates
        save_additional_profile_fields(
            cursor,
            existing_username,
            curr_phone,
            curr_a1,
            curr_a2,
            curr_city,
            curr_state,
            curr_country,
            curr_zip,
            curr_dob
        )
        conn.commit()
        # print("Profile updated successfully.")

        # cursor.execute('INSERT INTO users(user_name,user_pass,age,email_Id) VALUES(?,?,?,?)',(username,userpass,age,email))

        # conn.commit()
        # conn.close()
