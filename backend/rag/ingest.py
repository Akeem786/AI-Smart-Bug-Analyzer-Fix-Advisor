import os

from rag.chunking import Chunking
from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore


class IngestPipeline:

    def __init__(self):

        self.chunker = Chunking()

        self.embedding = EmbeddingModel()

        self.vector = VectorStore()

    def ingest(self, folder):

        idx = 0

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            if not os.path.isfile(path):

                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:

                text = f.read()

            chunks = self.chunker.split(text)

            embeddings = self.embedding.encode(chunks)

            ids = []

            docs = []

            vectors = []

            for chunk, emb in zip(chunks, embeddings):

                ids.append(str(idx))

                docs.append(chunk)

                vectors.append(emb.tolist())

                idx += 1

            self.vector.add(ids, docs, vectors)