from typing import Any, List, Dict
from rag.retriever import Retriever


class DuplicateAgent:
    """
    Duplicate Defect Search Agent.
    Searches the defect repository/vector database for previously resolved bugs
    with similar stack traces, error messages, or functional domains.
    """

    def __init__(self):
        self.retriever = Retriever()

    def analyze(self, input_data: Any) -> List[Dict[str, Any]]:
        query = ""
        if isinstance(input_data, dict):
            query = f"{input_data.get('bug_report', '')} {input_data.get('file_content', '')}"
        elif isinstance(input_data, str):
            query = input_data

        if not query.strip():
            return []

        return self.retriever.search(query, top_k=3)