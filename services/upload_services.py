from pathlib import Path
from fastapi import UploadFile

from app.ingestion.ingestion import ingest_pdf

Data = Path("data")
Data.mkdir(exist_ok=True)


async def upload_document(file: UploadFile):
    file_path = Data / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    ingest_pdf(file_path)
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
    }
