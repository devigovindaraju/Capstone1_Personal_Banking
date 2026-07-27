import streamlit as st
import requests


st.set_page_config(

    page_title="Upload Files",

    page_icon="📂"

)

import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSS_FILE = os.path.join(
    BASE_DIR,
    "static",
    "styles.css"
)

with open(
    CSS_FILE,
    "r",
    encoding="utf-8"
) as f:

    css = f.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="upload-title">
        Upload Documents
    </div>

    <div class="upload-subtitle">
        Upload documents to enhance the Personal Banking AI knowledge base
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(

    "Upload Document",

    type=[
        "pdf",
        "csv",
        "xlsx",
        "txt",
        "json"
    ]

)

if uploaded_file:

    if st.button("upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        try:

            response = requests.post(
                "http://localhost:9000/api/v1/documents/",
                files=files
            )

            response.raise_for_status()

            result = response.json()

            st.write(result["message"])
        except requests.exceptions.RequestException as e:

            st.error(
                f"Upload failed: {e}"
            )

