import os
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


class FileParser:
    """
    Robust file parser supporting .txt, .log, and .pdf files
    with multiple encoding fallbacks and size safety guards.
    """

    MAX_PREVIEW_CHARS = 100000

    @classmethod
    def parse(cls, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = os.path.splitext(file_path)[1].lower()

        if extension in [".txt", ".log"]:
            return cls._parse_text_file(file_path)
        elif extension == ".pdf":
            return cls._parse_pdf_file(file_path)
        else:
            # Attempt plain text read as fallback
            return cls._parse_text_file(file_path)

    @classmethod
    def _parse_text_file(cls, file_path: str) -> str:
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        content = None

        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    content = f.read()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if content is None:
            # Last resort: replace un-decodable bytes
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

        return cls._truncate_if_needed(content)

    @classmethod
    def _parse_pdf_file(cls, file_path: str) -> str:
        if PdfReader is None:
            return "[Error: PyPDF library is not available on the server]"

        try:
            reader = PdfReader(file_path)
            extracted_pages = []
            for idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(f"--- Page {idx + 1} ---\n{page_text.strip()}")

            if not extracted_pages:
                return "[Note: PDF contains no selectable text or scanned images]"

            full_text = "\n\n".join(extracted_pages)
            return cls._truncate_if_needed(full_text)
        except Exception as e:
            return f"[PDF Extraction Error: {str(e)}]"

    @classmethod
    def _truncate_if_needed(cls, text: str) -> str:
        if len(text) <= cls.MAX_PREVIEW_CHARS:
            return text

        head_len = cls.MAX_PREVIEW_CHARS // 2
        tail_len = cls.MAX_PREVIEW_CHARS // 2
        omitted = len(text) - (head_len + tail_len)
        return (
            text[:head_len]
            + f"\n\n... [Truncated {omitted} characters from middle of large log] ...\n\n"
            + text[-tail_len:]
        )