from rag.retriever import Retriever


class DuplicateAgent:

    def __init__(self):
        self.retriever = Retriever()

    def analyze(self, query):

        results = self.retriever.search(query)

        return results