from pathlib import Path
from fastapi import UploadFile

# from ingestion.ingestion import ingestion_document

Data = Path("data")
Data.mkdir(exist_ok=True)


async def upload_document(file: UploadFile):
    file_path = Data / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "saved_path": str(file_path),
        "exists": file_path.exists(),
    }
