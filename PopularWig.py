import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("Wig Popularity")

st.markdown("Our most popular wig based on our purchases right now is...")
conn2 = sqlite3.connect('OraWigs.db')  # open connection
cur2 = conn2.cursor()
df = pd.read_sql_query("SELECT Wig_Type, COUNT(*) as count FROM Purchases GROUP BY Wig_Type", conn2)
fig = px.pie(df, values='count', names='Wig_Type', title='Wig types:')  # counting how many of same wig type to be able to make the pie chart
st.plotly_chart(fig)  # show the pie chart to the user
conn2.close()  # close connection

