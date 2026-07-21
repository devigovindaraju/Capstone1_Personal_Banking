import streamlit as st


st.set_page_config(

    page_title="Upload Files",

    page_icon="📂"

)



st.title(
    "📂 Upload Documents"
)



uploaded_file = st.file_uploader(

    "Choose a file",

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

