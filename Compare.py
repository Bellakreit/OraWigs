import re
import sys
import requests
from bs4 import BeautifulSoup
import json
import csv  # importing all the libraries needed
# compare page 

def scrape(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # fake user for browser
    results = []  # empty list for results

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
        description = product["tags"]
        price = "$" + product["variants"][0]["price"]  # price is inside variants with name price
        results.append([description, price])
    
    print(results)
        

def main():
    wigs = scrape("https://shaniwigs.com/collections/wigs")
    for wig in wigs:
        print(wig)
if __name__ == "__main__":
    main()