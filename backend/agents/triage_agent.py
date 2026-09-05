import re
from typing import Dict, Any


class TriageAgent:
    """
    Intelligent Triage Agent that evaluates software defect severity,
    priority (P0-P3), functional category, and operational risk.
    """

    CRITICAL_PATTERNS = [
        r"fatal", r"crash", r"oom", r"out\s+of\s+memory", r"heap\s+space",
        r"kernel\s+panic", r"segmentation\s+fault", r"segfault",
        r"data\s+loss", r"corruption", r"deadlock", r"security\s+vulnerability",
        r"rce", r"sql\s+injection", r"auth\s+bypass", r"emergency", r"p0"
    ]

    HIGH_PATTERNS = [
        r"nullpointerexception", r"null\s*pointer", r"connection\s+refused",
        r"timeout", r"timed\s+out", r"500\s+internal", r"bad\s+gateway",
        r"service\s+unavailable", r"pool\s+exhausted", r"broken\s+pipe",
        r"access\s+denied", r"unauthorized", r"forbidden", r"database\s+error",
        r"transaction\s+rollback", r"rate\s+limit", r"p1"
    ]

    LOW_PATTERNS = [
        r"typo", r"cosmetic", r"font", r"color", r"alignment", r"spacing",
        r"tooltip", r"minor", r"label", r"spelling", r"p3", r"ui\s+glitch"
    ]

    CATEGORY_PATTERNS = {
        "Database & Storage": [r"sql", r"database", r"postgres", r"mysql", r"mongo", r"redis", r"deadlock", r"transaction", r"pool\s+limit"],
        "Security & Authentication": [r"jwt", r"auth", r"token", r"forbidden", r"unauthorized", r"cors", r"csrf", r"permission", r"credential"],
        "Memory & Performance": [r"oom", r"memory", r"leak", r"cpu", r"timeout", r"slow", r"heap", r"garbage\s+collector", r"latency"],
        "Network & Connectivity": [r"connection", r"network", r"socket", r"http", r"502", r"504", r"gateway", r"dns", r"refused"],
        "Frontend & UI Rendering": [r"react", r"render", r"component", r"css", r"dom", r"hydration", r"undefined\s+\(reading", r"javascript", r"browser"],
        "API & Backend Integration": [r"fastapi", r"endpoint", r"route", r"payload", r"rest", r"request", r"response", r"json", r"serializer"],
        "Application Logic & Validation": [r"indexerror", r"keyerror", r"valueerror", r"typeerror", r"assertion", r"logic", r"validator"]
    }

    def analyze(self, input_data: Any) -> Dict[str, Any]:
        text = ""
        if isinstance(input_data, dict):
            text = f"{input_data.get('bug_report', '')} {input_data.get('file_content', '')}"
        elif isinstance(input_data, str):
            text = input_data

        text_lower = text.lower()

        # Severity determination
        if any(re.search(p, text_lower) for p in self.CRITICAL_PATTERNS):
            severity = "Critical"
            priority = "P0"
            risk_score = 95
            sla_target = "Immediate (< 2 hours)"
        elif any(re.search(p, text_lower) for p in self.HIGH_PATTERNS):
            severity = "High"
            priority = "P1"
            risk_score = 75
            sla_target = "Same Day (< 8 hours)"
        elif any(re.search(p, text_lower) for p in self.LOW_PATTERNS):
            severity = "Low"
            priority = "P3"
            risk_score = 25
            sla_target = "Next Sprint / Backlog"
        else:
            severity = "Medium"
            priority = "P2"
            risk_score = 50
            sla_target = "Standard (< 48 hours)"

        # Category determination
        matched_category = "General Software Defect"
        max_matches = 0
        for category, patterns in self.CATEGORY_PATTERNS.items():
            matches = sum(1 for p in patterns if re.search(p, text_lower))
            if matches > max_matches:
                max_matches = matches
                matched_category = category

        return {
            "severity": severity,
            "priority": priority,
            "category": matched_category,
            "risk_score": risk_score,
            "sla_target": sla_target,
            "impact_summary": f"Classified as {severity} ({priority}) impacting {matched_category}."
        }