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
                "source": str(file_path),
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

    vector_store = get_vector_store(collection_name="personalized_retail_banking")
    vector_store.add_documents(chunks)
