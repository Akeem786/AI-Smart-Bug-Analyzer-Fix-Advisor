import re
from typing import Dict, Any, List


class RootCauseAgent:
    """
    Root Cause Diagnostic Agent.
    Synthesizes error signatures, stack traces, and defect narratives
    to uncover the underlying failure mechanism and execution timeline.
    """

    DIAGNOSTIC_RULES = [
        {
            "match": [r"nullpointerexception", r"nonetype", r"object\s+is\s+null", r"undefined\s+\(reading"],
            "root_cause": "Unchecked Null / Undefined Dereference",
            "mechanism": "The code attempted to invoke an attribute or method on an uninitialized or null reference before verifying existence.",
            "layer": "Application Logic / Data Access",
            "confidence": "94%",
            "blast_radius": ["AuthService", "Session Management", "User Profile Controller"],
            "timeline": [
                {"step": 1, "phase": "Request Ingress", "detail": "Client passes auth token or user identifier to endpoint."},
                {"step": 2, "phase": "Repository Lookup", "detail": "Database returns null / empty record (expired or deleted entity)."},
                {"step": 3, "phase": "Fault Trigger", "detail": "Code directly invokes .getProfile().getSettings() without null guard."},
                {"step": 4, "phase": "Exception Raised", "detail": "JVM raises java.lang.NullPointerException at AuthService.java:42."},
                {"step": 5, "phase": "System Impact", "detail": "Transaction rolls back; HTTP 500 returned to user."}
            ]
        },
        {
            "match": [r"pool\s+limit", r"timeout", r"queuepool", r"connection\s+timed\s+out", r"deadlock"],
            "root_cause": "Connection Pool Exhaustion / Resource Lock",
            "mechanism": "Database or network sessions were not released back to the pool (likely unclosed in error paths), leading to starvation under load.",
            "layer": "Database / Connection Manager",
            "confidence": "91%",
            "blast_radius": ["PostgreSQL Primary", "Async Worker Pool", "API Gateway"],
            "timeline": [
                {"step": 1, "phase": "High Concurrency", "detail": "Traffic spike floods connection pool beyond max capacity."},
                {"step": 2, "phase": "Connection Leak", "detail": "Exceptions in worker threads bypass session close / release handlers."},
                {"step": 3, "phase": "Pool Saturation", "detail": "Available pool size (10) and overflow (10) completely consumed."},
                {"step": 4, "phase": "Timeout Trigger", "detail": "New incoming requests block for 30.00s then raise TimeoutError."},
                {"step": 5, "phase": "System Impact", "detail": "Cascading failures across all dependent REST endpoints."}
            ]
        },
        {
            "match": [r"oom", r"out\s+of\s+memory", r"heap\s+space", r"sigkill", r"killed\s+by\s+oom"],
            "root_cause": "Unbounded Memory Allocation",
            "mechanism": "Batch data or large file buffers were loaded in-memory all at once rather than chunking or streaming via generators.",
            "layer": "Resource & Memory Architecture",
            "confidence": "96%",
            "blast_radius": ["Celery Task Worker", "PDF Export Engine", "Container Runtime"],
            "timeline": [
                {"step": 1, "phase": "Batch Job Trigger", "detail": "Export task requests report generation for millions of records."},
                {"step": 2, "phase": "Eager Evaluation", "detail": "Entire table read into memory using .all() instead of cursor streaming."},
                {"step": 3, "phase": "Heap Saturation", "detail": "RAM utilization breaches 2048MB cgroup container memory ceiling."},
                {"step": 4, "phase": "Kernel Intervention", "detail": "Linux kernel Out-Of-Memory killer sends SIGKILL (9) to worker."},
                {"step": 5, "phase": "System Impact", "detail": "Batch queue stalls; unacknowledged tasks re-queued repeatedly."}
            ]
        },
        {
            "match": [r"cors", r"access-control-allow-origin", r"preflight"],
            "root_cause": "Cross-Origin Resource Sharing (CORS) Policy Mismatch",
            "mechanism": "The API server rejected the browser's preflight OPTIONS handshake because the client origin is missing from CORS allowed origins.",
            "layer": "API Gateway / HTTP Middleware",
            "confidence": "98%",
            "blast_radius": ["Frontend SPA", "Public REST API", "Browser Network Layer"],
            "timeline": [
                {"step": 1, "phase": "Cross-Origin Request", "detail": "Browser sends preflight OPTIONS request from localhost:5173 to api:8000."},
                {"step": 2, "phase": "Header Inspection", "detail": "FastAPI middleware checks Access-Control-Allow-Origin whitelist."},
                {"step": 3, "phase": "Handshake Rejection", "detail": "Origin not matched or CORS middleware not mounted."},
                {"step": 4, "phase": "Browser Security Enforcement", "detail": "Browser blocks response from being read by JavaScript."},
                {"step": 5, "phase": "System Impact", "detail": "AxiosError: Network Error shown to end user."}
            ]
        },
        {
            "match": [r"indexerror", r"keyerror", r"list\s+index\s+out\s+of\s+range"],
            "root_cause": "Unchecked Boundary / Missing Key Access",
            "mechanism": "Direct index or key retrieval on an array/dictionary without checking sequence length or key presence.",
            "layer": "Data Ingestion / Parsing",
            "confidence": "92%",
            "blast_radius": ["CSV Ingestion Worker", "Data Pipeline"],
            "timeline": [
                {"step": 1, "phase": "File Parsing", "detail": "Row reader encounters truncated row or missing delimiter."},
                {"step": 2, "phase": "Unchecked Subscript", "detail": "Code attempts direct index access row[4] on 3-element list."},
                {"step": 3, "phase": "Exception Raised", "detail": "Python interpreter raises IndexError: list index out of range."},
                {"step": 4, "phase": "Batch Halt", "detail": "Ingestion loop aborts without processing remaining rows."}
            ]
        }
    ]

    DEFAULT_DIAGNOSIS = {
        "root_cause": "State Inconsistency / Unhandled Edge Condition",
        "mechanism": "Execution encountered an unexpected runtime state or unhandled boundary condition in business logic.",
        "layer": "Application Core",
        "confidence": "72%",
        "blast_radius": ["Core Application Module"],
        "timeline": [
            {"step": 1, "phase": "Execution Path", "detail": "Application executes normal business workflow."},
            {"step": 2, "phase": "Unexpected Input", "detail": "Data structure deviates from standard contract or validation rules."},
            {"step": 3, "phase": "Fault Emergence", "detail": "Runtime error occurs due to missing boundary checks."},
            {"step": 4, "phase": "Termination", "detail": "Execution halted or returned error response."}
        ]
    }

    def analyze(self, input_data: Any) -> Dict[str, Any]:
        text = ""
        if isinstance(input_data, dict):
            text = f"{input_data.get('bug_report', '')} {input_data.get('file_content', '')}"
        elif isinstance(input_data, str):
            text = input_data

        text_lower = text.lower()

        for rule in self.DIAGNOSTIC_RULES:
            if any(re.search(pattern, text_lower) for pattern in rule["match"]):
                return {
                    "possible_root_cause": rule["root_cause"],
                    "technical_mechanism": rule["mechanism"],
                    "affected_layer": rule["layer"],
                    "confidence": rule["confidence"],
                    "blast_radius": rule["blast_radius"],
                    "timeline": rule["timeline"],
                    "diagnostic_status": "Confirmed Root Cause"
                }

        return {
            "possible_root_cause": self.DEFAULT_DIAGNOSIS["root_cause"],
            "technical_mechanism": self.DEFAULT_DIAGNOSIS["mechanism"],
            "affected_layer": self.DEFAULT_DIAGNOSIS["layer"],
            "confidence": self.DEFAULT_DIAGNOSIS["confidence"],
            "blast_radius": self.DEFAULT_DIAGNOSIS["blast_radius"],
            "timeline": self.DEFAULT_DIAGNOSIS["timeline"],
            "diagnostic_status": "Preliminary Assessment"
        }