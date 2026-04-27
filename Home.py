import streamlit as st
import sqlite3
# home page

st.title("ORA WIGS", text_alignment="center")  # setting title, header and subheader for home page
st.header("Luxury wigs made to feel completely you", text_alignment="center")
st.subheader("Effortless beauty, affordable luxury, high-end feel", text_alignment="center")

# click on text and sends you to the ora wigs instagram
st.markdown("[Follow us on Instagram](https://www.instagram.com/ora.wigs?igsh=NTc4MTIwNjQ2YQ==)", text_alignment="center")

def btnNewCustomer_Click():  # when the new customer button is clicked function
    st.session_state.show_form = True
    st.session_state.customer_type = "new"  # remember which button was clicked

def btnOldCustomer_Click():  # when the old customer button is clicked function
    st.session_state.show_form = True
    st.session_state.customer_type = "existing"  # keep track that the customer is existing one

btnNewCustomer = st.button("New Customer", type="primary", on_click=btnNewCustomer_Click)
btnOldCustomer = st.button("Existing Customer", type="primary", on_click=btnOldCustomer_Click)

if "show_form" not in st.session_state:  # default for the form is false until the button is clicked
    st.session_state.show_form = False

if "customer_type" not in st.session_state:  # keep track of customer type so we can use correct form
    st.session_state.customer_type = None

if st.session_state.show_form:

    if st.session_state.customer_type == "new":  # if customer is new bring the form so they can be added to database
        customerForm = st.form('Profile')
        customerForm.subheader("New Customer Profile")  # form subheader
        UserName = customerForm.text_input('User Name')  # form txt boxes to be filled by the user
        Password = customerForm.text_input('Password')
        FirstName = customerForm.text_input('First Name')
        LastName = customerForm.text_input('Last Name')
        Email = customerForm.text_input('Email')
        Phone = customerForm.text_input('Phone Number')
        if customerForm.form_submit_button("Save"):
            if not UserName or not Password or not FirstName or not LastName or not Email or not Phone:  # checking all fields are filled
                st.error("Please fill in all fields.")
            else:
                conn2 = sqlite3.connect('OraWigs.db')  # open connection
                cur2 = conn2.cursor()
                cur2.execute("""
                INSERT INTO Customers (UserName, Password, FirstName, LastName, Email, Phone)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (UserName, Password, FirstName, LastName, Email, Phone))
                conn2.commit()
                st.session_state.show_form = False  # closes form after saved
                conn2.close()  # close connection
                st.success("Profile saved!")


    elif st.session_state.customer_type == "existing":  # if the customer is existing then bring the form up
        loginForm = st.form('Login')
        loginForm.subheader("Existing Customer")  # form subheader
        UserName = loginForm.text_input('User Name')  # inputs the username and password and then will be looked up
        Password = loginForm.text_input('Password')
        if loginForm.form_submit_button("Login"):
            if not UserName or not Password:  # check if fields are empty
                st.error("Please fill in all fields.")
            else:
                # look up user in database
                conn2 = sqlite3.connect('OraWigs.db')  # open connection
                cur2 = conn2.cursor()
                cur2.execute("SELECT FirstName, LastName, Email, Phone FROM Customers WHERE UserName = ? AND Password = ?", 
                        (UserName, Password))
                customer = cur2.fetchone()
                conn2.close()  # close connection
                if customer:  # if a customer was found print success message
                    st.success(f"Welcome back {customer[0]} {customer[1]}!")
                    # customer[0] = FirstName
                    # customer[1] = LastName
                else:  # if customer was not found print error message
                    st.error("Username or password not found.")
            st.session_state.show_form = False  # closes form  after pressing login

