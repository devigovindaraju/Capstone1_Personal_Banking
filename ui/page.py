import streamlit as st
from component.chat_box import chat_box

st.set_page_config(page_title="GenAI Assistant", page_icon="🤖", layout="wide")


st.write("Welcome to your GenAI platform")

chat_box()
