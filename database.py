import os
import sqlite3
from utils import hash

# This function allows us not to have more than one instance of a class
def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


# This is our dayabase service
class DatabaseDriver(object):
    # Making connection with database and creating users table
    def __init__(self):
        print("HERE")
        self.conn = sqlite3.connect("payment_app.db", check_same_thread=False)
        self.create_user_table()

    # Creates a user table with : ID, Name, Username, Balance, Password, and email properties
    def create_user_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE user (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL,
                    USERNAME TEXT NOT NULL,
                    BALANCE INT NOT NULL,
                    PASSWORD TEXT,
                    EMAIL TEXT
                );
            """)
        except Exception as e:
            print(e)

    # Select query to get all the users
    def get_all_users(self):
        cursor = self.conn.execute("SELECT * FROM user;")
        users = []

        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})

        return users

    # Insert query to insert a user to the users table
    def insert_user_table(self, name, username, balance, password="", email =""):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user (NAME, USERNAME, BALANCE, PASSWORD,EMAIL) VALUES (?, ?, ?, ?, ?);", (name, username, balance, hash(password),email))
        self.conn.commit()
        return cur.lastrowid


    # Select query to get a wanted user
    def get_user_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM user WHERE ID = ?", (id,))

        for row in cursor:
            return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3], "password": row[4], "email": row[5]}

        return None

    # Update a user
    def update_user_by_id(self, id, name, username, balance, password="",email = ""):
        self.conn.execute("""
            UPDATE user 
            SET name = ?, username = ?, balance = ?, password = ?, email = ?
            WHERE id = ?;
        """, (name, username, balance, hash(password), email, id))
        self.conn.commit()

    # Delete a user
    def delete_user_by_id(self, id):
        self.conn.execute("""
            DELETE FROM user
            WHERE id = ?;        
        """, (id))
        self.conn.commit()

# Creating an instance of Database class
DatabaseDriver = singleton(DatabaseDriver)