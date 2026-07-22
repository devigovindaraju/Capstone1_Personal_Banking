import streamlit as st


def initialize_chat():

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []



def add_user_message(
        message,
        request=None
):

    st.session_state.chat_history.append(

        {
            "role":"user",
            "message":message,
            "request":request
        }

    )



def add_bot_message(message):

    st.session_state.chat_history.append(

        {
            "role":"assistant",
            "message":message
        }

    )



def get_history():

    return st.session_state.chat_history



def clear_history():

    st.session_state.chat_history=[]