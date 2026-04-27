import streamlit as st
import sqlite3
from openai import OpenAI
from openai import AzureOpenAI

# adding chatbot

openai_api_key = st.secrets["AZURE_OPENAI_API_KEY"]  # opening ai chat
openai_api_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]

client = AzureOpenAI(
    api_key=openai_api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=openai_api_endpoint
)

# header for the tutorial page
st.title("Ask Mrs. Wigs for tutorial on measuring your head")

if "messages" not in st.session_state:  # making sure history is remembered
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask for a head measuring tutorial"):  # setting a prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # stream goes here, only runs when user sends a message
    stream = client.chat.completions.create(
        model=st.secrets["AZURE_OPENAI_MODEL"],
        # the ai knows its role as a lady helping the client measure their heads for wigs
        messages=[
            {"role": "system", "content": "You are a friendly lady chatbot helping clients learn how to measure their head for wig."},
            *st.session_state.messages
        ],
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

