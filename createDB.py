import sqlite3

conn = sqlite3.connect('OraWigs.db')  # connecting to database
cur = conn.cursor()

# creating the table for customers
cur.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT NOT NULL,
    Password TEXT NOT NULL,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT NOT NULL,
    Phone TEXT NOT NULL
)
""")

cur.execute("SELECT COUNT(*) FROM Customers")
if cur.fetchone()[0] == 0:
    Customers = [  # list to be added to table
        (1, "Bellak", "Bella111", "Bella", "Kreitenberg", "Bella@kreit.net", "8184868879"),
        (2, "skreit", "shain123", "Shaindee", "Kreitenberg", "skreit@kreit.net", "3106330245"),
    ]
    cur.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?, ?)", Customers)  # insert values in customers list
    conn.commit()

# creating the table for purchases
cur.execute("""
CREATE TABLE IF NOT EXISTS Purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Wig_Type TEXT NOT NULL
)
""")

cur.execute("SELECT COUNT(*) FROM Purchases")
if cur.fetchone()[0] == 0:
    Purchases = [  # list to be added to table
        (1, "Bella", "kreitenberg", "Luxury long brunette"),
        (2, "Shaindee", "Kreitenberg", "short pixie"),
        (3, "Rachel", "Kreit", "Luxury long brunette"),
        (4, "Sarah", "leibowitz", "Honey Blonde mom length")
    ]
    cur.executemany("INSERT INTO Purchases VALUES (?, ?, ?, ?)", Purchases)  # insert values into purchases
    conn.commit()

conn.close()