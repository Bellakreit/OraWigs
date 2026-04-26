import sqlite3

conn = sqlite3.connect('OraWigs.db')  # connecting to database
cur = conn.cursor()

# creating the table
cur.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT NOT NULL,
    Phone TEXT NOT NULL
)
""")

cur.execute("SELECT COUNT(*) FROM Customers")
if cur.fetchone()[0] == 0:
    Customers = [  # list to be added to table
        (1, "Bella", "Kreitenberg", "Bella@kreit.net", "8184868879"),
        (2, "Shaindee", "Kreitenberg", "skreit@kreit.net", "3106330245"),
    ]
    cur.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?, ?)", Customers)  # insert values in customers list
    conn.commit()
