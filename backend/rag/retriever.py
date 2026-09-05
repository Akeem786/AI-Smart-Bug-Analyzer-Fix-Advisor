import json
import math
import os
import re
from typing import List, Dict, Any

try:
    from rag.embeddings import EmbeddingModel
    from rag.vector_store import VectorStore
    CHROMA_AVAILABLE = True
except Exception:
    CHROMA_AVAILABLE = False


class Retriever:
    """
    Hybrid Retriever for Defect Search & Duplicate Detection.
    Prefers ChromaDB Vector Search when available; falls back smoothly
    to an in-memory TF-IDF cosine similarity engine using datasets/known_defects.json.
    """

    def __init__(self):
        self.chroma_ready = False
        self.dataset_path = self._locate_dataset()
        self.known_defects = self._load_known_defects()

        if CHROMA_AVAILABLE:
            try:
                self.embedding = EmbeddingModel()
                self.vector = VectorStore()
                self.chroma_ready = True
            except Exception:
                self.chroma_ready = False

    def _locate_dataset(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate = os.path.join(base_dir, "datasets", "known_defects.json")
        if os.path.exists(candidate):
            return candidate
        # Check parent dir
        parent_candidate = os.path.join(os.path.dirname(base_dir), "datasets", "known_defects.json")
        if os.path.exists(parent_candidate):
            return parent_candidate
        return candidate

    def _load_known_defects(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.dataset_path):
            try:
                with open(self.dataset_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            return []

        # If ChromaDB is available and initialized, attempt vector search
        if self.chroma_ready:
            try:
                vector = self.embedding.encode([query])[0]
                results = self.vector.search(vector)
                if results and "documents" in results and results["documents"]:
                    # Return formatted vector results
                    formatted = []
                    docs = results["documents"][0]
                    ids = results.get("ids", [[]])[0]
                    distances = results.get("distances", [[]])[0] if "distances" in results else []
                    for i, doc in enumerate(docs):
                        score = 80
                        if i < len(distances) and distances[i] is not None:
                            score = max(10, min(99, int((1.0 - distances[i]) * 100)))
                        formatted.append({
                            "id": ids[i] if i < len(ids) else f"DEF-{i+1}",
                            "title": doc[:80] + "..." if len(doc) > 80 else doc,
                            "description": doc,
                            "similarity_score": f"{score}%",
                            "status": "Vector Match"
                        })
                    return formatted
            except Exception:
                pass

        # Fallback to in-memory TF-IDF / lexical similarity engine
        return self._lexical_search(query, top_k)

    def _lexical_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        if not self.known_defects:
            return []

        def tokenize(text: str) -> List[str]:
            words = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
            stop_words = {"the", "a", "an", "is", "in", "at", "of", "on", "and", "or", "for", "to", "with", "by"}
            return [w for w in words if w not in stop_words and len(w) > 2]

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        # Calculate TF-IDF vectors
        corpus_docs = []
        for bug in self.known_defects:
            combined = f"{bug.get('title', '')} {bug.get('description', '')} {bug.get('component', '')} {bug.get('stack', '')}"
            corpus_docs.append(tokenize(combined))

        # Document frequencies
        df = {}
        n_docs = len(corpus_docs)
        for doc in corpus_docs:
            unique_terms = set(doc)
            for term in unique_terms:
                df[term] = df.get(term, 0) + 1

        def compute_vector(tokens: List[str]) -> Dict[str, float]:
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            vec = {}
            for t, count in tf.items():
                idf = math.log((n_docs + 1) / (df.get(t, 0) + 1)) + 1
                vec[t] = count * idf
            return vec

        def cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
            dot = sum(v1[k] * v2.get(k, 0) for k in v1)
            norm1 = math.sqrt(sum(v ** 2 for v in v1.values()))
            norm2 = math.sqrt(sum(v ** 2 for v in v2.values()))
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot / (norm1 * norm2)

        q_vec = compute_vector(query_tokens)
        scores = []
        for idx, doc_tokens in enumerate(corpus_docs):
            doc_vec = compute_vector(doc_tokens)
            sim = cosine_similarity(q_vec, doc_vec)
            scores.append((sim, self.known_defects[idx]))

        scores.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, bug in scores[:top_k]:
            pct = int(min(98, max(20, sim * 100 + (25 if sim > 0 else 0))))
            results.append({
                "id": bug.get("id", "BUG-UNKNOWN"),
                "title": bug.get("title", "Untitled Defect"),
                "component": bug.get("component", "General"),
                "stack": bug.get("stack", "N/A"),
                "severity": bug.get("severity", "Medium"),
                "similarity_score": f"{pct}%",
                "root_cause": bug.get("root_cause", ""),
                "resolution": bug.get("resolution", ""),
                "description": bug.get("description", "")
            })

        return results