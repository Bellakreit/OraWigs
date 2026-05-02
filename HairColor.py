import streamlit as st
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
# hair color page, scrape the hair color info from wiki how website 
# and store it in database and then display it on my streamlit app

def createTable():  # making the table to store the scraped data
    conn = sqlite3.connect("OraWigs.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HairColorTips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            heading TEXT,
            tip TEXT
        )
    """)
    conn.commit()
    conn.close()

# scraping the data and storing each step with its explanation into the table
def scrapeAndStore():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://www.wikihow.com/Choose-Hair-Color-for-Skin-Tone", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    conn = sqlite3.connect("OraWigs.db")
    cur = conn.cursor()

    # clear old data so we don't get duplicates on re-scrape
    cur.execute("DELETE FROM HairColorTips")

    steps = soup.find_all("div", class_="step")  # finding the div class="step" on the page because thats what each step is called
    for step in steps:  # goes thru each step
        heading = step.find("b")  #finds the header that has the tag </b>
        text = step.get_text(strip=True)  # gets all the text that was in step tahts in a simple string
        if heading:  # only if the step has a </b> tag then...
            heading_text = heading.get_text(strip=True)   # get the text of the heading
            # remove the repeated heading from the start of the tip because it repeats it there too
            tip = text.replace(heading_text, "", 1).strip()
            # remove reference markers like [3]XResearch source or [5]XExpert Source where they have references at the bottom
            tip = re.sub(r'\[\d+\]X\w+\s*\w*', '', tip).strip()  # uses re to find all of them and erase them
            # the r makes this into a regular string so the regex characters are treated literal now. the [\d+] is how the reference is written like [5] and it always has an X after with a few words
            # use this query to insert the heading and tip into the table we created
            cur.execute(
                "INSERT INTO HairColorTips (heading, tip) VALUES (?, ?)",
                (heading_text, tip)
            )

    conn.commit()
    conn.close()

# retreiving the info from the database with a query
def getInfo():
    conn = sqlite3.connect("OraWigs.db")
    cur = conn.cursor()
    cur.execute("SELECT heading, tip FROM HairColorTips")
    rows = cur.fetchall()
    conn.close()
    return rows


# designing the page
st.title("Hair Color for Your Skin Tone")
st.markdown("how to choose a hair color that suits you best")
createTable()  # call the method to create the table in th database
scrapeAndStore()   # call method to scrape the data and store it

info = getInfo()  # get the lists of tuples from the database and store in variable

for heading, tip in info:  # for every header and tip display it on the page
    st.subheader(heading)
    st.write(tip)