import sys
import sqlite3
from state import state
from rich.console import Console
from rich.table import Table
from Choice import get_choice
from datetime import datetime


# print("Times accepted.")


def manage_inventory():

    conn = sqlite3.connect("airline.db")
    cursor = conn.cursor()

    # def is_leap_year(year):
    #     return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def insert_carrier_details():
        while True:

            cursor.execute("SELECT * FROM Carriers")
            rows=cursor.fetchall()

            table = Table(title="Carriers")
            columns = [desc[0] for desc in cursor.description] 


            for col in columns:
                table.add_column(col,style="cyan")

            for row in rows:
                table.add_row(*map(str,row))
            console=Console()
            console.print(table)
            
            try:
                carrier_id = int(input("Enter Carrier ID: "))
                if (carrier_id < 0):
                    print(f"Enter proper values only") 
                    continue
                cursor.execute("SELECT carrier_id FROM Carriers")
                rows=cursor.fetchall()
                carrierList=[row[0] for row in rows]
                if carrier_id in carrierList:
                    print("Carrier already exists 🙏 ...only unique entries allowed")
                    continue

            except Exception as e:
                print(f"An exception occurred")
                continue
            except KeyboardInterrupt as e:
                sys.exit()

            break

        

        while True:
            try:
                carrier_name = input("Enter Carrier Name: ")
                if not carrier_name.isalpha():
                    print("Enter values from  A to Z and a to z ...")
                    continue
           
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            break

            
        while True:
            try:
                refund_2 = int(input("Refund % before 2 days: "))
                if(refund_2 <= 20 or refund_2 >40 ):
                    print("Only between 20 to 40")
                    continue
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            break

        while True:
            try:
                refund_10 = int(input("Refund % before 10 days: "))
                if(refund_10 <= 40 or refund_10 > 60):
                    print("Only between 40 to 60")
                    continue
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            break

        while True:
            try:
                refund_20 = int(input("Refund % before 20 days: "))
                if(refund_20 < 60 or refund_20 > 90):
                    print("Only between 60 to 90")
                    continue
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            break

        # while True:
        #     try:
        #         silver_discount = int(input("Discount for silver user % : "))
        #         if(silver_discount <= 1 or silver_discount>5):
        #             print("Only between 1 to 5")
        #             continue
        #     except Exception as e:
        #         print(e)
        #         continue
        #     except KeyboardInterrupt as e:
        #         sys.exit()
        #     break
        
        # while True:
        #     try:
        #         gold_discount = int(input("Discount for gold user %: "))
        #         if(gold_discount <= 6 or gold_discount>10):
        #             print("Only between 6 to 10")
        #             continue
        #     except Exception as e:
        #         print(e)
        #         continue
        #     except KeyboardInterrupt as e:
        #         sys.exit()
        #     break

        while True:
            try:
                flight_id = int(input("Enter Flight ID: "))
                if flight_id<1:
                    print("Enter valid value...")
                    continue
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            break
        
       
        
       
        while True:
            try:
                start_time = datetime.strptime(input("Enter start time (HH:MM): ").strip(), "%H:%M").time()
            except ValueError:
                print("Re-enter time details in correct format hr(00-23):min(00-59)")
                continue

            try:
                end_time = datetime.strptime(input("Enter end time (HH:MM): ").strip(), "%H:%M").time()
            except ValueError:
                print("Re-enter time details in correct format hr(00-23):min(00-59)")
                continue

            except KeyboardInterrupt as e:
                sys.exit()

            if start_time > end_time:
                print("Error: start time cannot be later than end time (same day).")
                continue

            break
    
        while True:
            try:

                date_input = input("Enter Date of Journey (DD-MM-YYYY): ").strip()
                
                journey_date_obj = datetime.strptime(date_input, "%d-%m-%Y")
               
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
              
                if journey_date_obj.year != 2026:
                    print("❌ Date must be in the year 2026 only.")
                    continue

                if journey_date_obj < today:
                    print("❌ Date cannot be in the past.")
                    continue

                date_of_journey = journey_date_obj.strftime("%d-%m-%Y")
                break

            except ValueError:
                print("❌ Invalid format! Enter date as DD-MM-YYYY.")
            except KeyboardInterrupt:
                sys.exit()


                
                    
               
                    
                # except ValueError:
                #     print("Enter only string values")
                # except Exception as e:
                #     print(e)
                #     continue
                # except KeyboardInterrupt as e:
                #     sys.exit()

        # Check if flight exists
        cursor.execute(
            "SELECT flight_id FROM Flights WHERE flight_id = ?",
            (flight_id,)
        )

        # console=Console()
        flight_row = cursor.fetchone()
        if flight_row:
            flight=flight_row[0]
        else:
            flight=None


        # table = Table(title="Flights")
        # columns = [desc[0] for desc in cursor.description] 

        # for col in columns:
        #     table.add_column(col,style="cyan")

        # for row in rows:
        #     table.add_row(*map(str,row))


        # flight_ids=cursor.fetchone()
        # flight=flight_ids[0]

# I AM FINDING THE FLIGHT ID , IF THE FLIGHT EXISTS
#  THEN I FETCH THE ID OF THAT FLIGHT AND I CREATE A NEW CARRIER ELSE,
# I CREATE A COMPLETELY NEW FLIGHT AND THEN ADD THE CARRIER

        if flight:
            print("Flight exists...fetching flight_id")
            rows=cursor.fetchall()
            list_of_carriers = [row[0] for row in rows]
            if carrier_id not in list_of_carriers:

                # cursor.execute(
                #     """
                #     INSERT INTO Carriers (
                #         Carrier_Id,
                #         Carrier_name,
                #         refund_before_2days_Of_travel,
                #         refund_before_10days_Of_travel,
                #         refund_before_20days_Of_travel,
                #         silver_user_discount,
                #         gold_user_discount,
                #         flight_id,
                #         start_time,
                #         end_time

                #     )
                #     VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)
                #     """,
                #     (
                #         carrier_id,
                #         carrier_name,
                #         refund_2,
                #         refund_10,
                #         refund_20,
                #         silver_discount,
                #         gold_discount,
                #         flight,
                #         str(start_time),
                #         str(end_time)
                #     )
                # )

                cursor.execute(
                    """
                    INSERT INTO Carriers (
                        Carrier_Id,
                        Carrier_name,
                        refund_before_2days_Of_travel,
                        refund_before_10days_Of_travel,
                        refund_before_20days_Of_travel,
                        flight_id,
                        start_time,
                        end_time,
                        date_of_journey

                    )
                    VALUES (?, ?, ?, ?, ?, ?,?,?,?)
                    """,
                    (
                        carrier_id,
                        carrier_name,
                        refund_2,
                        refund_10,
                        refund_20,
                        flight,
                        str(start_time),
                        str(end_time),
                        date_of_journey
                    )
                )

            conn.commit()
            print("✅ Carrier inserted successfully.")

        cursor.execute("SELECT * FROM Carriers")
        rows=cursor.fetchall()

        table = Table(title="Carriers")
        columns = [desc[0] for desc in cursor.description] 


        for col in columns:
            table.add_column(col,style="cyan")

        for row in rows:
            table.add_row(*map(str,row))
        console=Console()
        console.print(table)

        cursor.execute("SELECT flight_id FROM Flights")
        row=cursor.fetchall()
        flight_ids=row[0]            

        if not flight:
            print("⚠️ Flight does not exist. Creating new flight entry.")

            while True:
                try:
                    flight_id = int(input("Enter flight id: "))
                    if flight_id in flight_ids:
                        print("Flight ID already exists...")
                        continue
                    elif flight_id<1:
                        print("Enter valid flight value")
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
                break

            while True:
                try:
                    flight_name = input("Enter Flight Name: ")
                    if not flight_name.isalpha():
                        print("Enter values from  A to Z and a to z ...")
                        continue
            
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
                break

            while True:
                try:
                    start_loc = input("Enter Start Location: ")
                    if not start_loc.isalpha():
                        print("Enter values from  A to Z and a to z ...")
                        continue
                
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
            
                try:
                    end_loc = input("Enter end Location: ")
                    if not end_loc.isalpha():
                        print("Enter values from  A to Z and a to z ...")
                        continue
              
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
                if start_loc==end_loc:
                    print("CHOOSE WISELY 😒...Destination and source cannot be the same")
                    continue
                break
            

            while True:
                try:
                    base_price = int(input("Enter base price: "))
                    if base_price < 1:
                        print("Enter valid value...")
                        continue
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
                break

            while True:
                try:
                    economy_no_of_seats= int(input("Enter Number of economy seats: "))
                    if economy_no_of_seats<1:
                        print("Enter valid value...")
                        continue
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
                break

            while True:
                try:
                    business_no_of_seats= int(input("Enter Number of business seats: "))
                    if business_no_of_seats<1:
                        print("Enter valid value...")
                        continue
                except Exception as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    sys.exit()
                break

           # PRINT ALL THE FLIGHTS AND CARRIERS THAT HAVE BEEN ADDED 

            cursor.execute(
                """
                INSERT INTO Flights(
                flight_id,
                flight_name,
                start_loc,
                end_loc,
                base_price,
                economy_no_of_seats,
                business_no_of_seats,
                economy_available_seats,
                business_available_seats
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                flight_id,
                flight_name,
                start_loc,
                end_loc,
                base_price,
                economy_no_of_seats,
                business_no_of_seats,
                economy_no_of_seats,
                business_no_of_seats
                )
            )

            conn.commit()
            print("✅ Flight created successfully.")

            cursor.execute("SELECT * FROM Flights")
            rows=cursor.fetchall()

                    ###### FLIGHTS ######
                    
            table = Table(title="Flights")
            columns = [desc[0] for desc in cursor.description] 

            for col in columns:
                table.add_column(col,style="cyan")

            for row in rows:
                table.add_row(*map(str,row))
            console=Console()
            console.print(table)

                    ###### CARRIERS ######

            cursor.execute("SELECT * FROM Carriers")
            rows=cursor.fetchall()

            table = Table(title="Carriers")
            columns = [desc[0] for desc in cursor.description] 


            for col in columns:
                table.add_column(col,style="cyan")

            for row in rows:
                table.add_row(*map(str,row))
            console=Console()
            console.print(table)

            # END OF PRINT SECTION


        # Insert carrier
        cursor.execute(
            '''
            SELECT Carrier_Id FROM Carriers
            '''
        )
        
        rows=cursor.fetchall()
        list_of_carriers = [row[0] for row in rows]
        if carrier_id not in list_of_carriers:

            # cursor.execute(
            #     """
            #     INSERT INTO Carriers (
            #         Carrier_Id,
            #         Carrier_name,
            #         refund_before_2days_Of_travel,
            #         refund_before_10days_Of_travel,
            #         refund_before_20days_Of_travel,
            #         silver_user_discount,
            #         gold_user_discount,
            #         flight_id,
            #         start_time,
            #         end_time

            #     )
            #     VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)
            #     """,
            #     (
            #         carrier_id,
            #         carrier_name,
            #         refund_2,
            #         refund_10,
            #         refund_20,
            #         silver_discount,
            #         gold_discount,
            #         flight_id,
            #         str(start_time),
            #         str(end_time)
            #     )
            # )

            cursor.execute(
                """
                INSERT INTO Carriers(
                    Carrier_Id,
                    Carrier_name,
                    refund_before_2days_Of_travel,
                    refund_before_10days_Of_travel,
                    refund_before_20days_Of_travel,
                    flight_id,
                    start_time,
                    end_time,
                    date_of_journey
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
                """,
                (
                    carrier_id,
                    carrier_name,
                    refund_2,
                    refund_10,
                    refund_20,
                    flight_id,
                    str(start_time),
                    str(end_time),
                    date_of_journey
                )
            )

        conn.commit()
        print("✅ Carrier inserted successfully.")

    def remove_carrier_details():
        cursor.execute("SELECT * FROM Carriers")
        carrier_details = cursor.fetchall()

        table = Table(title="Carriers Data")

        columns = [desc[0] for desc in cursor.description]
        for col in columns:
            table.add_column(col, style="cyan")

        for carrier in carrier_details:
            table.add_row(*map(str, carrier))

        console = Console()
        console.print(table)
        
        while True:
            try:
                carrier_id = int(input("Enter Carrier ID to remove: "))
                if(carrier_id<1):
                    print("Non negative integers only...")
                    continue
            except Exception as e:
                print(e)
                continue
            except KeyboardInterrupt as e:
                sys.exit()
            break


        cursor.execute(
            """
            DELETE FROM Carriers
            WHERE Carrier_Id = ?
            """,
            (carrier_id,)
        )

        if cursor.rowcount == 0:
            print("❌ No carrier found with given Carrier ID and Flight ID.")
        else:
            conn.commit()
            print("✅ Carrier removed successfully.")

        confirmation_msg = input("Do you want to continue removing other carriers as well? Enter y for yes, n for No: ")
        if confirmation_msg.lower() == 'y':
            return True
        elif confirmation_msg.lower() == 'n':
            return False
        else:
            return False

    while True:
        print("\n--- Manage Inventory ---")
        print("1--->Insert Carrier Details")
        print("2--->Remove Carrier Details")
        print("3--->Back")

        try:
            choice = get_choice()

        except KeyboardInterrupt:
            sys.exit()

        if choice == 1:
            insert_carrier_details()
        elif choice == 2:
            while True:
                msg = remove_carrier_details()
                if msg == False:
                    break
        elif choice == 3:
            break
        else:
            print("❌ Invalid choice")

    conn.close()

# import sys
# import sqlite3
# from state import state
# from rich.console import Console
# from rich.table import Table
# from Choice import get_choice
# from datetime import datetime


# def manage_inventory():

#     conn = sqlite3.connect("airline.db")
#     conn.execute("PRAGMA foreign_keys = ON")
#     cursor = conn.cursor()

#     console = Console()

#     def insert_carrier_details():

#         # ================= CARRIER INPUT =================

#         while True:
#             try:
#                 carrier_id = int(input("Enter Carrier ID: "))
#                 if carrier_id < 1:
#                     print("Enter proper values only")
#                     continue
#                 break
#             except:
#                 print("Invalid input")

#         while True:
#             carrier_name = input("Enter Carrier Name: ")
#             if not carrier_name.isalpha():
#                 print("Enter values from A to Z only")
#                 continue
#             break

#         def get_positive_int(msg):
#             while True:
#                 try:
#                     value = int(input(msg))
#                     if value < 1:
#                         print("Enter valid value...")
#                         continue
#                     return value
#                 except:
#                     print("Invalid input")

#         refund_2 = get_positive_int("Refund % before 2 days: ")
#         refund_10 = get_positive_int("Refund % before 10 days: ")
#         refund_20 = get_positive_int("Refund % before 20 days: ")
#         silver_discount = get_positive_int("Discount for silver user %: ")
#         gold_discount = get_positive_int("Discount for gold user %: ")

#         # ================= TIME INPUT =================

#         while True:
#             try:
#                 start_time = datetime.strptime(
#                     input("Enter start time (HH:MM): "), "%H:%M"
#                 ).time()
#                 end_time = datetime.strptime(
#                     input("Enter end time (HH:MM): "), "%H:%M"
#                 ).time()

#                 if start_time > end_time:
#                     print("Start time cannot be later than end time")
#                     continue
#                 break
#             except:
#                 print("Enter time in HH:MM format")

#         # ================= DISPLAY FLIGHTS =================

#         cursor.execute("SELECT flight_id, flight_name, start_loc, end_loc FROM Flights")
#         flights = cursor.fetchall()

#         table = Table(title="Flights")
#         table.add_column("Flight ID", style="cyan")
#         table.add_column("Flight Name", style="cyan")
#         table.add_column("Start", style="cyan")
#         table.add_column("End", style="cyan")

#         for row in flights:
#             table.add_row(*map(str, row))

#         console.print(table)

#         # ================= ROUTE INPUT =================

#         start_loc = input("Enter Start Location: ").strip()
#         end_loc = input("Enter End Location: ").strip()

#         if start_loc.lower() == end_loc.lower():
#             print("Source and destination cannot be same")
#             return

#         # ================= CHECK IF FLIGHT EXISTS =================

#         cursor.execute("""
#             SELECT flight_id FROM Flights
#             WHERE lower(start_loc)=? AND lower(end_loc)=?
#         """, (start_loc.lower(), end_loc.lower()))

#         flight_row = cursor.fetchone()

#         if flight_row:
#             flight_id = flight_row[0]
#             print("✅ Flight exists. Using existing flight ID:", flight_id)

#         else:
#             print("⚠️ Flight does not exist. Creating new flight...")

#             flight_name = input("Enter Flight Name: ")
#             base_price = get_positive_int("Enter base price: ")
#             economy_seats = get_positive_int("Enter economy seats: ")
#             business_seats = get_positive_int("Enter business seats: ")

#             cursor.execute("""
#                 INSERT INTO Flights (
#                     flight_name, start_loc, end_loc,
#                     base_price,
#                     economy_no_of_seats,
#                     business_no_of_seats,
#                     economy_available_seats,
#                     business_available_seats
#                 )
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 flight_name,
#                 start_loc,
#                 end_loc,
#                 base_price,
#                 economy_seats,
#                 business_seats,
#                 economy_seats,
#                 business_seats
#             ))

#             conn.commit()
#             flight_id = cursor.lastrowid
#             print("✅ Flight created with ID:", flight_id)

#         # ================= CHECK CARRIER DUPLICATE =================

#         cursor.execute("SELECT carrier_id FROM Carriers WHERE carrier_id = ?", (carrier_id,))
#         existing = cursor.fetchone()

#         if existing:
#             print("❌ Carrier ID already exists.")
#             return

#         # ================= INSERT CARRIER =================

#         cursor.execute("""
#             INSERT INTO Carriers (
#                 carrier_id,
#                 carrier_name,
#                 refund_before_2days_of_travel,
#                 refund_before_10days_of_travel,
#                 refund_before_20days_of_travel,
#                 silver_user_discount,
#                 gold_user_discount,
#                 flight_id,
#                 start_time,
#                 end_time
#             )
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             carrier_id,
#             carrier_name,
#             refund_2,
#             refund_10,
#             refund_20,
#             silver_discount,
#             gold_discount,
#             flight_id,
#             str(start_time),
#             str(end_time)
#         ))

#         conn.commit()
#         print("✅ Carrier inserted successfully.")

#     # ================= REMOVE CARRIER =================

#     def remove_carrier_details():

#         cursor.execute("SELECT * FROM Carriers")
#         carriers = cursor.fetchall()

#         table = Table(title="Carriers Data")
#         columns = [desc[0] for desc in cursor.description]
#         for col in columns:
#             table.add_column(col, style="cyan")

#         for row in carriers:
#             table.add_row(*map(str, row))

#         console.print(table)

#         try:
#             carrier_id = int(input("Enter Carrier ID to remove: "))
#         except:
#             print("Invalid input")
#             return False

#         cursor.execute("DELETE FROM Carriers WHERE carrier_id=?", (carrier_id,))

#         if cursor.rowcount == 0:
#             print("❌ No carrier found.")
#         else:
#             conn.commit()
#             print("✅ Carrier removed successfully.")

#         return input("Remove more? (y/n): ").lower() == "y"

#     # ================= MENU LOOP =================

#     while True:
#         print("\n--- Manage Inventory ---")
#         print("1. Insert Carrier Details")
#         print("2. Remove Carrier Details")
#         print("3. Back")

#         try:
#             choice = get_choice()
#         except KeyboardInterrupt:
#             sys.exit()

#         if choice == 1:
#             insert_carrier_details()
#         elif choice == 2:
#             while remove_carrier_details():
#                 pass
#         elif choice == 3:
#             break
#         else:
#             print("❌ Invalid choice")

#     conn.close()
