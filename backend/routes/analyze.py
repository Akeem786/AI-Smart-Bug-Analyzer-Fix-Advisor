from fastapi import APIRouter

from agents.triage_agent import TriageAgent
from agents.log_analysis_agent import LogAnalysisAgent
from agents.root_cause_agent import RootCauseAgent
from agents.duplicate_agent import DuplicateAgent
from agents.remediation_agent import RemediationAgent

router = APIRouter()


@router.post("/analyze")

def analyze_bug(data: dict):

    triage = TriageAgent().analyze(data)

    logs = LogAnalysisAgent().analyze(
        data.get("bug_report", "")
    )

    root = RootCauseAgent().analyze(data)

    duplicate = DuplicateAgent().analyze(
        data.get("bug_report", "")
    )

    remediation = RemediationAgent().analyze()

    return {

        "triage": triage,

        "log_analysis": logs,

        "root_cause": root,

        "duplicate_bugs": duplicate,

        "remediation": remediation
    }