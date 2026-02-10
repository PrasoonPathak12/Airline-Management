import sqlite3 as sql
import bcrypt

conn=sql.connect('airline.db')
cursor=conn.cursor()

user_name=input("Enter user name: \n")
user_pass=input("Enter account password: \n")

userPassword =cursor.execute('SELECT user_pass FROM Users WHERE user_name=?',(user_name))

if(user_pass==userPassword):
    print("Welcome ",user_name)
else:
    print("No such user exists...")
conn.commit()
conn.close()