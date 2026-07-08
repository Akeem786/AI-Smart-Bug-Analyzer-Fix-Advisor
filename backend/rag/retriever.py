from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.embedding = EmbeddingModel()

        self.vector = VectorStore()

    def search(self, query):

        vector = self.embedding.encode([query])[0]

        return self.vector.search(vector)