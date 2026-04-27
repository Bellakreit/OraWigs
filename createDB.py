import sqlite3
import requests
from bs4 import BeautifulSoup
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
#adding purchases records in
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

#function for scraping the website
def scrape():
    headers = {"User-Agent": "Mozilla/5.0"}  # fake user for browser
    results = []  # empty list for results
    # oras is array of prices based on the json I made an array in order of the json products with accurate prices of ora wigs to compare to the other brand wigs
    oras = ["$1500.00", "$2000.00", "$1200.00", "$2150.00", "$1750.00", "$1750.00", "$1000.00", "$1200.00", "$2500.00", "$2000.00", "$1500.00"]
    response = requests.get(  # get the website
        "https://shaniwigs.com/collections/wigs/products.json?limit=250",
        headers=headers
    )
    # use BeautifulSoup to parse the response text
    soup = BeautifulSoup(response.text, "html.parser")
 
    # extract the text content and parse as JSON
    data = json.loads(soup.get_text())
    # do this to see the data formatted nicely
    # print(json.dumps(data, indent=2))
    
    for product in data["products"]:
        description = ", ".join(product["tags"])
        # stores as string for database
        price = "$" + product["variants"][0]["price"]  # price is inside variants with name price
        results.append([description, price])
    paired = []
    for result, ora_price in zip(results, oras):  # zip will pair the ora price to each result by position in array and will only do the amount of ora prices I put in
        result.append(ora_price)  # add in the ora price
        paired.append(result)  # add the paired result to the paired list
    
    return paired  # only returns the wigs that have ora prices

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
    ComparePrice = scrape()  # the list to be added to the table is what was scraped from "https://shaniwigs.com/collections/wigs"
    cur.executemany("INSERT INTO ComparePrice VALUES (?, ?, ?)", ComparePrice)  # insert values into ComparePrice table
    conn.commit()


conn.close()