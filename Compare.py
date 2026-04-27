import streamlit as st
import sqlite3
import pandas as pd
# compare page 

st.title("Compare Our Price")

st.markdown("At Ora Wigs you get luxury Wigs for a fraction of the price")
st.markdown("look at the table below to see other brands prices compared to our price for the same wig!")
conn2 = sqlite3.connect('OraWigs.db')  # open connection
cur2 = conn2.cursor()
# get the information from ComparePrice table, and change the name of fields so it is user friendly
df = pd.read_sql_query(""" 
    SELECT 
        Description AS 'Wig Details',
        OtherBrands AS 'Other Brands Price', 
        OraPrice AS 'Ora Wigs Price' 
    FROM ComparePrice
""", conn2)
st.dataframe(df)  # put into a data frame to be viewed easily by the user
