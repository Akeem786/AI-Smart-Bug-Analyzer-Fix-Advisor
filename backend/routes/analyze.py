import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form

from agents.triage_agent import TriageAgent
from agents.log_analysis_agent import LogAnalysisAgent
from agents.root_cause_agent import RootCauseAgent
from agents.duplicate_agent import DuplicateAgent
from agents.remediation_agent import RemediationAgent
from services.file_parser import FileParser

router = APIRouter(tags=["Defect Analysis"])

UPLOAD_FOLDER = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/analyze")
def analyze_bug(data: Dict[str, Any]):
    """
    Analyzes submitted bug report and/or extracted file content
    using multi-agent intelligence pipeline.
    """
    bug_report = data.get("bug_report", "")
    file_content = data.get("file_content", "")

    combined_context = f"{bug_report}\n\n{file_content}".strip()
    analysis_payload = {
        "bug_report": bug_report,
        "file_content": file_content,
        "combined": combined_context
    }

    triage = TriageAgent().analyze(analysis_payload)
    logs = LogAnalysisAgent().analyze(analysis_payload)
    root = RootCauseAgent().analyze(analysis_payload)
    duplicate = DuplicateAgent().analyze(analysis_payload)
    remediation = RemediationAgent().analyze(analysis_payload)

    return {
        "status": "success",
        "triage": triage,
        "log_analysis": logs,
        "root_cause": root,
        "duplicate_bugs": duplicate,
        "remediation": remediation
    }


@router.post("/submit-and-analyze")
async def submit_and_analyze_bug(
    bug_report: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    Single-step endpoint: Uploads and parses file, then runs all AI agents.
    """
    uploaded_file = None
    extracted_text = ""
    file_size = 0

    if file and file.filename:
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

    analysis_payload = {
        "bug_report": bug_report,
        "file_content": extracted_text
    }

    triage = TriageAgent().analyze(analysis_payload)
    logs = LogAnalysisAgent().analyze(analysis_payload)
    root = RootCauseAgent().analyze(analysis_payload)
    duplicate = DuplicateAgent().analyze(analysis_payload)
    remediation = RemediationAgent().analyze(analysis_payload)

    return {
        "status": "success",
        "message": "Bug Report Analyzed Successfully",
        "bug_report": bug_report,
        "uploaded_file": uploaded_file,
        "file_size_bytes": file_size,
        "file_content": extracted_text,
        "triage": triage,
        "log_analysis": logs,
        "root_cause": root,
        "duplicate_bugs": duplicate,
        "remediation": remediation
    }