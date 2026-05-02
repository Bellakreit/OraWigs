import streamlit as st
# streamlit run OraWigs_app.py to run app
Home_page = st.Page("Home.py", title="Home Page")  # creat home page
PopularWig_page = st.Page("PopularWig.py", title="Most Popular Wig Page")  # create popular wig page
Compare_page = st.Page("Compare.py", title="Compare Page")  # create compare page
Order_page = st.Page("Order.py", title="Order Page")  # create order page
Tutorial_page = st.Page("Tutorial.py", title="Tutorial Page")  # create tutorial page
HairColor_page = st.Page("HairColor.py", title="Hair Color Page")  # create hair color page
pg = st.navigation([Home_page, PopularWig_page, Compare_page, Order_page, Tutorial_page, HairColor_page])  # make a navigation for the pages
st.set_page_config(page_title="Ora Wigs")  # keep browser consistent
pg.run()
