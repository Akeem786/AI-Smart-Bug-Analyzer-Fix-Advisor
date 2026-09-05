import re
from typing import Dict, Any, List


class RemediationAgent:
    """
    Remediation & Fix Advisory Agent.
    Produces step-by-step technical instructions, code patch examples,
    unified diffs, and downloadable patch content.
    """

    REMEDIATIONS = [
        {
            "match": [r"nullpointerexception", r"nonetype", r"undefined\s+\(reading"],
            "recommendation": "Implement strict null/undefined guards and optional chaining prior to property dereference.",
            "target_file": "AuthService.java",
            "language": "java",
            "before_code": "public Settings getUserSettings(User user) {\n    return user.getProfile().getSettings();\n}",
            "after_code": "public Settings getUserSettings(User user) {\n    if (user == null || user.getProfile() == null) {\n        throw new EntityNotFoundException(\"User or profile reference is missing\");\n    }\n    return user.getProfile().getSettings();\n}",
            "diff_lines": [
                {"type": "context", "text": " public Settings getUserSettings(User user) {"},
                {"type": "removed", "text": "-    return user.getProfile().getSettings();"},
                {"type": "added",   "text": "+    if (user == null || user.getProfile() == null) {"},
                {"type": "added",   "text": "+        throw new EntityNotFoundException(\"User or profile reference is missing\");"},
                {"type": "added",   "text": "+    }"},
                {"type": "added",   "text": "+    return user.getProfile().getSettings();"},
                {"type": "context", "text": " }"}
            ],
            "steps": [
                "Verify entity existence immediately following database/repository retrieval.",
                "Use defensive programming (e.g. Optional.ofNullable in Java, Optional Chaining ?. in JS, if obj is not None: in Python).",
                "Add explicit schema validation so upstream services cannot pass null payloads for required fields."
            ],
            "preventive_actions": [
                "Configure static analysis linters (SonarQube, NullAway, ESLint) to flag unhandled nulls.",
                "Adopt non-nullable types in TypeScript or Python typing.Optional."
            ]
        },
        {
            "match": [r"pool\s+limit", r"timeout", r"queuepool", r"deadlock"],
            "recommendation": "Safeguard connection lifecycle with deterministic context managers and adjust pool thresholds.",
            "target_file": "database/session.py",
            "language": "python",
            "before_code": "def get_active_items():\n    session = SessionLocal()\n    items = session.query(Item).all()\n    return items  # Session left unclosed!",
            "after_code": "async def get_active_items():\n    async with get_db_session() as session:\n        async with session.begin():\n            result = await session.execute(select(Item))\n            return result.scalars().all()  # Automatically cleaned up",
            "diff_lines": [
                {"type": "removed", "text": "-def get_active_items():"},
                {"type": "removed", "text": "-    session = SessionLocal()"},
                {"type": "removed", "text": "-    items = session.query(Item).all()"},
                {"type": "removed", "text": "-    return items"},
                {"type": "added",   "text": "+async def get_active_items():"},
                {"type": "added",   "text": "+    async with get_db_session() as session:"},
                {"type": "added",   "text": "+        async with session.begin():"},
                {"type": "added",   "text": "+            result = await session.execute(select(Item))"},
                {"type": "added",   "text": "+            return result.scalars().all()"}
            ],
            "steps": [
                "Audit code to ensure all DB sessions are encapsulated in try/finally or 'with session:' context blocks.",
                "Increase max_overflow and pool_size in database engine configuration.",
                "Set pool_recycle and pool_pre_ping to automatically drop stale dropped connections."
            ],
            "preventive_actions": [
                "Establish connection pool telemetry with Prometheus / Grafana alerts on pool utilization > 80%.",
                "Tune query timeouts so hanging queries fail fast instead of holding connections indefinitely."
            ]
        },
        {
            "match": [r"oom", r"out\s+of\s+memory", r"heap\s+space", r"sigkill"],
            "recommendation": "Transition from eager in-memory loading to streaming or chunked generator pipelines.",
            "target_file": "workers/export_worker.py",
            "language": "python",
            "before_code": "def export_all_logs():\n    records = db.query(LogRecord).all()  # Crashes RAM with millions of rows\n    return generate_pdf(records)",
            "after_code": "def export_all_logs():\n    with tempfile.NamedTemporaryFile() as tmp:\n        for chunk in db.query(LogRecord).yield_per(1000):\n            stream_chunk_to_file(tmp, chunk)\n        return send_file(tmp.name)",
            "diff_lines": [
                {"type": "context", "text": " def export_all_logs():"},
                {"type": "removed", "text": "-    records = db.query(LogRecord).all()"},
                {"type": "removed", "text": "-    return generate_pdf(records)"},
                {"type": "added",   "text": "+    with tempfile.NamedTemporaryFile() as tmp:"},
                {"type": "added",   "text": "+        for chunk in db.query(LogRecord).yield_per(1000):"},
                {"type": "added",   "text": "+            stream_chunk_to_file(tmp, chunk)"},
                {"type": "added",   "text": "+        return send_file(tmp.name)"}
            ],
            "steps": [
                "Refactor queries to use pagination or streaming cursors (e.g. yield_per(1000)).",
                "For file uploads/PDF generation, stream directly to disk or S3 without buffering entire byte arrays.",
                "Explicitly invoke garbage collection gc.collect() after intensive batch operations."
            ],
            "preventive_actions": [
                "Define strict memory limits and requests in Docker / Kubernetes cgroups.",
                "Set worker_max_memory_per_child to auto-recycle background workers upon threshold breach."
            ]
        },
        {
            "match": [r"cors", r"access-control-allow-origin"],
            "recommendation": "Register CORSMiddleware on the backend router with explicit origin whitelists.",
            "target_file": "main.py",
            "language": "python",
            "before_code": "from fastapi import FastAPI\n\napp = FastAPI()\n# Missing CORS Middleware!",
            "after_code": "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI()\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\"http://localhost:5173\", \"http://127.0.0.1:5173\"],\n    allow_credentials=True,\n    allow_methods=[\"*\"],\n    allow_headers=[\"*\"],\n)",
            "diff_lines": [
                {"type": "context", "text": " from fastapi import FastAPI"},
                {"type": "added",   "text": "+from fastapi.middleware.cors import CORSMiddleware"},
                {"type": "context", "text": " "},
                {"type": "context", "text": " app = FastAPI()"},
                {"type": "added",   "text": "+app.add_middleware("},
                {"type": "added",   "text": "+    CORSMiddleware,"},
                {"type": "added",   "text": "+    allow_origins=[\"http://localhost:5173\", \"http://127.0.0.1:5173\"],"},
                {"type": "added",   "text": "+    allow_credentials=True,"},
                {"type": "added",   "text": "+    allow_methods=[\"*\"],"},
                {"type": "added",   "text": "+    allow_headers=[\"*\"],"},
                {"type": "added",   "text": "+)"}
            ],
            "steps": [
                "Import CORSMiddleware from fastapi.middleware.cors.",
                "Add middleware to the FastAPI application instance.",
                "Specify frontend domain origins, methods=['*'], and allow_credentials=True."
            ],
            "preventive_actions": [
                "Avoid wildcard '*' origins in production when using cookie or header-based credentials.",
                "Use environment variables to inject allowed domains dynamically."
            ]
        }
    ]

    DEFAULT_REMEDIATION = {
        "recommendation": "Apply boundary validation, structured error logging, and write regression test cases.",
        "target_file": "service/handler.py",
        "language": "python",
        "before_code": "def process_request(payload):\n    return execute_action(payload)",
        "after_code": "def process_request(payload):\n    try:\n        validate_payload(payload)\n        return execute_action(payload)\n    except ValidationError as err:\n        logger.warning(f\"Validation rejected: {err}\")\n        raise HTTPException(status_code=400, detail=str(err))",
        "diff_lines": [
            {"type": "context", "text": " def process_request(payload):"},
            {"type": "removed", "text": "-    return execute_action(payload)"},
            {"type": "added",   "text": "+    try:"},
            {"type": "added",   "text": "+        validate_payload(payload)"},
            {"type": "added",   "text": "+        return execute_action(payload)"},
            {"type": "added",   "text": "+    except ValidationError as err:"},
            {"type": "added",   "text": "+        logger.warning(f\"Validation rejected: {err}\")"},
            {"type": "added",   "text": "+        raise HTTPException(status_code=400, detail=str(err))"}
        ],
        "steps": [
            "Reproduce the defect locally in an isolated integration test.",
            "Verify all external inputs with strict Pydantic or schema validators.",
            "Add defensive exception handling around vulnerable call sites."
        ],
        "preventive_actions": [
            "Increase automated test coverage on edge cases.",
            "Enable continuous monitoring with error tracking tools (e.g. Sentry)."
        ]
    }

    def analyze(self, input_data: Any = None) -> Dict[str, Any]:
        text = ""
        if isinstance(input_data, dict):
            text = f"{input_data.get('bug_report', '')} {input_data.get('file_content', '')}"
        elif isinstance(input_data, str):
            text = input_data

        text_lower = text.lower()

        chosen = self.DEFAULT_REMEDIATION
        for rem in self.REMEDIATIONS:
            if any(re.search(pattern, text_lower) for pattern in rem["match"]):
                chosen = rem
                break

        # Generate unified patch string
        patch_str = f"--- a/{chosen['target_file']}\n+++ b/{chosen['target_file']}\n"
        for dl in chosen["diff_lines"]:
            patch_str += f"{dl['text']}\n"

        return {
            "recommendation": chosen["recommendation"],
            "target_file": chosen["target_file"],
            "language": chosen["language"],
            "before_code": chosen["before_code"],
            "after_code": chosen["after_code"],
            "diff_lines": chosen["diff_lines"],
            "patch_file_content": patch_str,
            "code_patch": chosen["after_code"],
            "remediation_steps": chosen["steps"],
            "preventive_actions": chosen["preventive_actions"]
        }