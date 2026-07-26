import streamlit as st
import requests

st.set_page_config(page_title="Upload Files", page_icon="📂")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS_FILE = os.path.join(BASE_DIR, "static", "styles.css")

with open(CSS_FILE, "r", encoding="utf-8") as f:

    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="upload-title">
        Upload Documents
    </div>

    <div class="upload-subtitle">
        Upload documents to enhance the Personal Banking AI knowledge base
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("", type=["pdf", "csv", "xlsx", "txt", "json"])


if uploaded_file:

    st.success(f"{uploaded_file.name} uploaded successfully")
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

    response = requests.post("http://localhost:8000/api/v1/documents/", files=files)

    if response.status_code == 200:
        st.success("File uploaded successfully!")
        st.json(response.json())
    else:
        st.error("Upload failed")
        st.write(response.text)
