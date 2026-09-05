import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.file_parser import FileParser

router = APIRouter(tags=["Bug Submission"])

UPLOAD_FOLDER = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/submit")
async def submit_bug(
    bug_report: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    uploaded_file = None
    extracted_text = ""
    file_size = 0

    if file and file.filename:
        # Sanitize filename
        safe_filename = os.path.basename(file.filename)
        uploaded_file = safe_filename
        file_path = UPLOAD_FOLDER / safe_filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_size = os.path.getsize(file_path)
            extracted_text = FileParser.parse(str(file_path))
        except Exception as e:
            extracted_text = f"File parsing error: {str(e)}"

    return {
        "status": "success",
        "message": "Bug Report Submitted Successfully",
        "bug_report": bug_report,
        "uploaded_file": uploaded_file,
        "file_size_bytes": file_size,
        "file_content": extracted_text,
        "extracted_chars": len(extracted_text)
    }