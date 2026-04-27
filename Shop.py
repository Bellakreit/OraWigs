import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("Shop Page")

st.markdown("Our most popular wig based on our purchases right now is...")
conn2 = sqlite3.connect('OraWigs.db')  # open connection
cur2 = conn2.cursor()
df = pd.read_sql_query("SELECT Wig_Type, COUNT(*) as count FROM Purchases GROUP BY Wig_Type", conn2)
fig = px.pie(df, values='count', names='Wig_Type', title='Wig types:')
st.plotly_chart(fig)
conn2.close()  # close connection

