from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from app.core.db import get_vector_store

load_dotenv()


def ingest_pdf(file_path):
    print("Ingestion Started")

    # 1.load pdf
    try:
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
    except Exception as e:
        print("Failed to load documents")
        raise RuntimeError("Document loading failed") from e

    # 3 Chunking
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.split_documents(docs)
        print("Total chunks")
        print(len(chunks))
    except Exception as e:
        print("Failed to split documents")
        raise RuntimeError("Document chunking failed") from e

    try:
        vector_store = get_vector_store(collection_name="personalized_retail_banking")
        vector_store.add_documents(chunks)
        return "Documents ingested successfully"
    except Exception as e:
        print("Failed to ingest documents")
        raise RuntimeError("Failed to ingest documents") from e
