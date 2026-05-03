import sqlite3
import requests
import json

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
# adding customer values/records in
cur.execute("SELECT COUNT(*) FROM Customers")
if cur.fetchone()[0] == 0:
    Customers = [  # list to be added to table
        (1, "Bellak", "Bella111", "Bella", "Kreit", "Bella@gmail.com", "8184869999"),
        (2, "skreit", "shain123", "Shaindee", "Kreit", "sk@gmail.net", "31039380245"),
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
#adding purchases records in
cur.execute("SELECT COUNT(*) FROM Purchases")
if cur.fetchone()[0] == 0:
    Purchases = [  # list to be added to table
        (1, "Bella", "kreit", "Luxury long brunette"),
        (2, "Shaindee", "Kreit", "short pixie"),
        (3, "Rachel", "Kreit", "Luxury long brunette"),
        (4, "Sarah", "leiba", "Honey Blonde mom length")
    ]
    cur.executemany("INSERT INTO Purchases VALUES (?, ?, ?, ?)", Purchases)  # insert values into purchases
    conn.commit()

#function for scraping the website
def getAPI():
    headers = {"User-Agent": "Mozilla/5.0"}  # fake user for browser
    # oras is array of prices based on the json I made an array in order of the json products with accurate prices of ora wigs to compare to the other brand wigs
    oras = ["$1500.00", "$2000.00", "$1200.00", "$2150.00", "$1750.00", "$1750.00", "$1000.00", "$1200.00", "$2500.00", "$2000.00", "$1500.00"]
    
    try:
        response = requests.get(  # get the website
            "https://shaniwigs.com/collections/wigs/products.json?limit=250",
            headers=headers
        )
        response.raise_for_status()  # raises an error if the request failed
        # parse as JSON because the content of the website is in JSON format
        data = response.json()
        
        paired = []
        for product, ora_price in zip(data["products"], oras):  # zip will pair the ora price to each result by position in array and will only do the amount of ora prices I put in
            description = ", ".join(product["tags"])
            price = "$" + product["variants"][0]["price"]  # price is inside variants with name price
            paired.append([description, price, ora_price])  # add the paired result to the paired list
        
        return paired  # only returns the wigs that have ora prices
    
    except requests.exceptions.HTTPError as e:  # if the request fails
        print(f"Error: Bad response from shaniwigs.com: {e}")
        return []  # returns the empty list so program doesnt crash at when this function is called
    except (KeyError, ValueError) as e:  # make sure data is found and in correct format
        print(f"Error: Could not parse product data: {e}")
        return []
     

# creating the table for compare page
cur.execute("""
CREATE TABLE IF NOT EXISTS ComparePrice (
    Description TEXT NOT NULL,
    OtherBrands TEXT NOT NULL,
    OraPrice TEXT NOT NULL
)
""")
#adding description price of other brand and price of ora wigs to the table
cur.execute("SELECT COUNT(*) FROM ComparePrice")
if cur.fetchone()[0] == 0:
    ComparePrice = getAPI()  # the list to be added to the table is what was scraped from "https://shaniwigs.com/collections/wigs"
    if ComparePrice:  # only insert if we got data back
        cur.executemany("INSERT INTO ComparePrice VALUES (?, ?, ?)", ComparePrice)  # insert values into ComparePrice table
        conn.commit()
    else:  # to warn that nothing was entered since scrape did not work
        print("Warning: No data was inserted into ComparePrice — scrape returned empty.")

conn.close()