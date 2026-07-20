# Load the pdf file from the data folder
# extract the content of the file
# arrive at the chunking strategy
# load the embedding model
# embed the chunks
# connect to postgres and activate pgvector extension
# save the vector embeddings and original text in db

# uv add python-dotenv
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from app.core.db import get_vector_store

load_dotenv()


def ingest_pdf(file_path):
    print("Ingestion Started")

    # 1.load pdf
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2.metadata enrichment (for citation)
    for doc in docs:
        doc.metadata.update(
            {
                "source": file_path,
                "document_extension": "pdf",
                "page": doc.metadata.get("page"),
                "last_updated": os.path.getmtime(file_path),
            }
        )
    print(docs)
    print("Before Chunking")

    # 3 Chunking

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(docs)
    print("Total chunks")
    print(len(chunks))

    # 4 load the embedding model & 5 generate the embeddings
    # 6. save it in vector db
    vector_store = get_vector_store(collection_name="personalized_retail_banking")
    vector_store.add_documents(chunks)


ingest_pdf("data/Capstone_Project_2_Personalized_Retail_Banking_FAQ.pdf")

# to run the script
# uv run python -m app.ingestion.ingestion
