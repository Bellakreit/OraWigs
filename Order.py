import streamlit as st
import sqlite3

st.title("Order Now")

def CustomOrder_Click():  # when the old customer button is clicked function
    st.session_state.show_form = True
    # st.session_state.customer_type = "existing"  # keep track that the customer is existing one

def buildEmailBody(color, length, texture, hairtype, wigtype, lining, head, front, ear): # build the email body string. Raises ValueError if any field is empty
    if not color or not length or not texture or not hairtype or not wigtype or not lining or not head or not front or not ear:
        raise ValueError("Please fill in all fields.")
    # body takes all the fields and put them into a message that will be sent in the email, %0A is a line break in the email and %0A%0A is to skip a line
    body = f"Hi Ora Wigs, I would like to place a custom order with the following details:%0A%0AColor: {color}%0ALength: {length} inches%0ATexture: {texture}%0AHair Type: {hairtype}%0AWig Type: {wigtype}%0ALining: {lining}%0A%0AMeasurements:%0AHead Circumference: {head} cm%0AFront to Back: {front} cm%0AEar to Ear: {ear} cm%0A%0AThank you!"
    return body

btnCustomOrder = st.button("Make a Custom Order", type="primary", on_click=CustomOrder_Click)

if "show_form" not in st.session_state:  # default for the form is false until the button is clicked
    st.session_state.show_form = False

if st.session_state.show_form:  # if the button was clicked for custom order then show the form
    with st.form("Custom_form"):  # made the form
        st.write("Custom Order Form, fill in details below and then click below to send your order to us!")
        my_color = st.text_input("Color: ")  # all the text boxes for the details of the wig
        my_length = st.text_input("Length (inches): ")
        my_texture = st.selectbox('Pick a texture', ['straight','wavy','curly', 'other'], index=None)  # index none makes the default none of options so that the user has to pick one
        my_hairtype = st.selectbox('Pick a hair type', ['Brazillian(coarser/thicker)','European(finer/silky)'], index=None)
        my_wigtype = st.selectbox('Pick a wig type', ['Full lace','Lace front','fall','hat fall'],  index=None)
        my_lining = st.selectbox('Pick a lining type', ['no lining', 'yes lining'], index=None)
        st.write("Measurements (go to tutorial page to learn how to measure your head):")
        my_head = st.text_input("Head circumference (cm): ")
        my_front = st.text_input("Front to back (cm): ")
        my_ear = st.text_input("Ear to ear (cm): ")
        if st.form_submit_button('press here to get button to send your order in'):
            try:
                body = buildEmailBody(my_color, my_length, my_texture, my_hairtype, my_wigtype, my_lining, my_head, my_front, my_ear)
                st.markdown(f'<a href="mailto:bella@kreit.net?subject=Wig Inquiry&body={body}">Click Here to send your order</a>', unsafe_allow_html=True)
                # it will send to bella@kreit.net with the subject and body filled in
                # you click on click here to send your order and it will take you to your email, unsafe_allow_html=True so that streamlit will allow outside websites
            except ValueError as e:
                st.error(str(e))
