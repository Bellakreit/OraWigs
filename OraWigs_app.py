import streamlit as st
# streamlit run OraWigs_app.py to run app
Home_page = st.Page("Home.py", title="Home Page")  # creat home page
Shop_page = st.Page("Shop.py", title="Shop Page")  # create shop page
pg = st.navigation([Home_page, Shop_page])  # make a navigation for the pages
st.set_page_config(page_title="Ora Wigs")  # keep browser consistent
pg.run()
