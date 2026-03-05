from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from datetime import datetime

from app.services.ingest_service import ingest_uploaded_file

router = APIRouter()

DATA_DIR = "data"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".txt", ".pdf")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.makedirs(DATA_DIR, exist_ok=True)

    file_path = os.path.join(DATA_DIR, file.filename)

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    result = ingest_uploaded_file(file_path)

    return result