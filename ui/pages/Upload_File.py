import streamlit as st


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

    "",

    type=[
        "pdf",
        "csv",
        "xlsx",
        "txt",
        "json"
    ]

)



if uploaded_file:


    st.success(

        f"{uploaded_file.name} uploaded successfully"

    )


    # Here you can add:
    #
    # - save file
    # - vector database ingestion
    # - RAG pipeline

