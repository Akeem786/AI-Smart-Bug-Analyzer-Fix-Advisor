import chromadb


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="vector_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="bugs"
        )

    def add(self, ids, documents, embeddings):

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings
        )

    def search(self, embedding):

        return self.collection.query(

            query_embeddings=[embedding],

            n_results=5
        )