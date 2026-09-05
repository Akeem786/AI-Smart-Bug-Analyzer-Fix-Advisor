import re
from typing import Dict, Any, List


class LogAnalysisAgent:
    """
    Intelligent Log & Stack Trace Analysis Agent.
    Identifies exceptions, parses stack frames, line numbers, and error signatures.
    """

    KNOWN_EXCEPTIONS = [
        r"(java\.lang\.[A-Za-z0-9_]+Exception)",
        r"(java\.lang\.[A-Za-z0-9_]+Error)",
        r"([A-Za-z0-9_]+Error)(?::\s*|\s*\n)",
        r"([A-Za-z0-9_]+Exception)(?::\s*|\s*\n)",
        r"(NullPointerException)",
        r"(TypeError)",
        r"(ValueError)",
        r"(IndexError)",
        r"(KeyError)",
        r"(TimeoutError)",
        r"(ConnectionRefusedError)",
        r"(OutOfMemoryError)",
        r"(CORS\s+policy\s+blocked)",
        r"(AxiosError)",
        r"(HTTP\s+\d{3}\s+[A-Za-z\s]+)",
        r"(500\s+Internal\s+Server\s+Error)",
        r"(502\s+Bad\s+Gateway)"
    ]

    STACK_PATTERNS = [
        r"Traceback \(most recent call last\):",
        r"\sat\s+[\w\.\$]+\([\w\.]+:\d+\)",
        r"\sat\s+[\w\.\$]+\s+\([^)]+:\d+:\d+\)",
        r"File \"[^\"]+\", line \d+",
        r"Exception in thread \"[^\"]+\""
    ]

    def analyze(self, input_data: Any) -> Dict[str, Any]:
        text = ""
        if isinstance(input_data, dict):
            text = f"{input_data.get('bug_report', '')}\n{input_data.get('file_content', '')}"
        elif isinstance(input_data, str):
            text = input_data

        if not text.strip():
            return {
                "error_detected": False,
                "error_type": "None",
                "stack_trace_found": False,
                "detected_exceptions": [],
                "stack_frames": [],
                "log_level_counts": {"ERROR": 0, "WARN": 0, "INFO": 0, "FATAL": 0},
                "summary": "No logs or bug text provided."
            }

        # Check for stack trace presence
        has_stack_trace = any(re.search(p, text) for p in self.STACK_PATTERNS)

        # Detect exceptions
        detected_exceptions: List[str] = []
        for pattern in self.KNOWN_EXCEPTIONS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                clean = m.strip()
                if clean and clean not in detected_exceptions:
                    detected_exceptions.append(clean)

        primary_error = detected_exceptions[0] if detected_exceptions else (
            "Generic Runtime Error" if has_stack_trace else "Unspecified Defect"
        )

        # Extract file locations and line numbers
        stack_frames = []
        python_frames = re.findall(r'File "([^"]+)", line (\d+)(?:, in (\w+))?', text)
        for f in python_frames:
            stack_frames.append({
                "file": f[0],
                "line": f[1],
                "function": f[2] if len(f) > 2 and f[2] else "N/A",
                "type": "Python Frame"
            })

        java_frames = re.findall(r'at ([\w\.\$]+)\(([\w\.]+):(\d+)\)', text)
        for f in java_frames:
            stack_frames.append({
                "file": f[1],
                "line": f[2],
                "function": f[0],
                "type": "Java Frame"
            })

        js_frames = re.findall(r'at\s+(?:async\s+)?([^\s\(\)]+)\s*\((.+?):(\d+):(\d+)\)', text)
        for f in js_frames:
            stack_frames.append({
                "file": f[1],
                "line": f[2],
                "function": f[0],
                "type": "JavaScript/Node Frame"
            })

        # Count log levels
        log_counts = {
            "FATAL": len(re.findall(r"\b(FATAL|CRITICAL)\b", text, re.IGNORECASE)),
            "ERROR": len(re.findall(r"\b(ERROR|FAIL|FAILED)\b", text, re.IGNORECASE)),
            "WARN": len(re.findall(r"\b(WARN|WARNING)\b", text, re.IGNORECASE)),
            "INFO": len(re.findall(r"\bINFO\b", text))
        }

        error_detected = len(detected_exceptions) > 0 or has_stack_trace or log_counts["ERROR"] > 0

        return {
            "error_detected": error_detected,
            "error_type": primary_error,
            "stack_trace_found": has_stack_trace,
            "detected_exceptions": detected_exceptions[:5],
            "stack_frames": stack_frames[:8],
            "log_level_counts": log_counts,
            "summary": f"Detected error signature '{primary_error}' with {len(stack_frames)} extracted stack frames." if error_detected else "No definitive exception pattern detected in text."
        }