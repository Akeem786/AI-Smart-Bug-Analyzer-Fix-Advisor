from fastapi import APIRouter, UploadFile, File, Form
from services.file_parser import FileParser
import shutil
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/submit")
async def submit_bug(
    bug_report: str = Form(...),
    file: UploadFile = File(None)
):
    uploaded_file = None
    extracted_text = ""

    if file:
        uploaded_file = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            extracted_text = FileParser.parse(file_path)
        except Exception as e:
            extracted_text = f"File parsing error: {str(e)}"

    return {
        "message": "Bug Submitted Successfully",
        "bug_report": bug_report,
        "uploaded_file": uploaded_file,
        "file_content": extracted_text
    }