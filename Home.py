import streamlit as st
import sqlite3
# home page

st.title("ORA WIGS", text_alignment="center")  # setting title, header and subheader for home page
st.header("Luxury wigs made to feel completely you", text_alignment="center")
st.subheader("Effortless beauty, affordable luxury, high-end feel", text_alignment="center")

# click on text and sends you to the ora wigs instagram
st.markdown("[Follow us on Instagram](https://www.instagram.com/ora.wigs?igsh=NTc4MTIwNjQ2YQ==)", text_alignment="center")

conn = sqlite3.connect('OraWigs.db')  # connecting to database
cur = conn.cursor()

def btnNewCustomer_Click():  # when the new customer button is clicked function
    pass

def btnOldCustomer_Click():  # when the old customer button is clicked function
    pass

btnNewCustomer = st.button("New Customer", type="primary", on_click=btnNewCustomer_Click)
btnOldCustomer = st.button("Existing Customer", type="primary", on_click=btnOldCustomer_Click)

customerForm = st.form('Profile')
customerForm.subheader("Profile")
FirstName = customerForm.text_input('First Name')
LastName = customerForm.text_input('Last Name')
Email = customerForm.text_input('Email')
Phone = customerForm.text_input('Phone Number')
customerForm.form_submit_button("Save")
# with st.form("customerForm"):
#     st.write("Profile")
#     FirstName = st.text_input('First Name')
#     st.label("click save to ecplore the rest of the site")
#     st.form_submit_button('Save Profile')

