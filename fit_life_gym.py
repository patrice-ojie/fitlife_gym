"""The purpose of this program is to create a demo version of a membership management system for a gym called FitLife"""

import sqlite3
from datetime import datetime


class FitLifeGym:
    def __init__(self):
        # Establish connection to the SQLite database
        self.conn = sqlite3.connect('fitlife.db')
        # Create necessary tables if they don't exist
        self.create_tables()

    def create_tables(self):
        # Create tables for members, classes, memberships, and attendance
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            email TEXT,
                            phone TEXT,
                            membership_status INTEGER
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            date TEXT,
                            time TEXT,
                            instructor TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS memberships (
                            member_id INTEGER,
                            start_date TEXT,
                            end_date TEXT,
                            PRIMARY KEY (member_id),
                            FOREIGN KEY (member_id) REFERENCES members(id)
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                            member_id INTEGER,
                            class_id INTEGER,
                            attendance_date TEXT,
                            PRIMARY KEY (member_id, class_id),
                            FOREIGN KEY (member_id) REFERENCES members(id),
                            FOREIGN KEY (class_id) REFERENCES classes(id)
                          )''')
        # Commit changes to the database
        self.conn.commit()

    def register_member(self, name, email, phone):
        # Insert member details into the members table
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO members (name, email, phone, membership_status) 
                          VALUES (?, ?, ?, ?)''', (name, email, phone, 1))
        # Commit changes to the database
        self.conn.commit()
        # Return the ID of the newly registered member
        return cursor.lastrowid

    def schedule_class(self, class_name, class_date, class_time, instructor):
        # Insert class details into the classes table
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO classes (name, date, time, instructor) 
                          VALUES (?, ?, ?, ?)''', (class_name, class_date, class_time, instructor))
        # Commit changes to the database
        self.conn.commit()
        # Return the ID of the newly scheduled class
        return cursor.lastrowid

    def renew_membership(self, member_id):
        # Update membership status to indicate renewal
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE members SET membership_status = 1 WHERE id = ?''', (member_id,))
        # Commit changes to the database
        self.conn.commit()

    def enroll_member_in_class(self, member_id, class_id):
        # Record member attendance for a specific class
        cursor = self.conn.cursor()
        attendance_date = datetime.now().strftime('%d-%m-%Y')
        cursor.execute('''INSERT INTO attendance (member_id, class_id, attendance_date) 
                          VALUES (?, ?, ?)''', (member_id, class_id, attendance_date))
        # Commit changes to the database
        self.conn.commit()

    def get_member_details(self, member_id):
        # Retrieve member details from the members table
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM members WHERE id = ?''', (member_id,))
        # Return member details as a tuple
        return cursor.fetchone()

    def get_class_details(self, class_id):
        # Retrieve class details from the classes table
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM classes WHERE id = ?''', (class_id,))
        # Return class details as a tuple
        return cursor.fetchone()


# Demo example of 2 hypothetical members
fitlife = FitLifeGym()

# Register members
member1_id = fitlife.register_member("John Doe", "john@hotmail.com", "+447123456789")
member2_id = fitlife.register_member("Alice Smith", "alice@gmail.com", "+447987654321")

# Schedule classes
class1_id = fitlife.schedule_class("Yoga", "18-03-2024", "10:00 AM", "Instructor A")
class2_id = fitlife.schedule_class("Zumba", "20-03-2024", "5:00 PM", "Instructor B")

# Renew memberships
fitlife.renew_membership(member1_id)

# Enroll members in classes
fitlife.enroll_member_in_class(member1_id, class1_id)
fitlife.enroll_member_in_class(member2_id, class2_id)

# Get member and class details
print("Member Details:")
print(fitlife.get_member_details(member1_id))
print("\nClass Details:")
print(fitlife.get_class_details(class1_id))
