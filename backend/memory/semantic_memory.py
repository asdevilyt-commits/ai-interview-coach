import math
from typing import List, Dict, Any, Optional
from backend.core.logger import logger


class SemanticVectorMemory:
    """
    Tier 2 — Semantic Memory (Vector Store).
    Stores vector embeddings for past answers, interview notes, resume snippets, and mistakes.
    Guarantees strict tenant isolation by filtering documents by candidate_id.
    """
    def __init__(self):
        self._store: List[Dict[str, Any]] = []

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in text.split() if len(w) > 2]

    def add_document(self, candidate_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        doc = {
            "candidate_id": candidate_id,
            "content": content,
            "metadata": metadata or {},
            "tokens": set(self._tokenize(content)),
        }
        self._store.append(doc)
        logger.info(f"Added document to Semantic Memory for candidate '{candidate_id}'. Total docs: {len(self._store)}")

    def search(self, candidate_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_tokens = set(self._tokenize(query))
        if not query_tokens:
            return []

        results = []
        for doc in self._store:
            # Candidate Data Isolation Check
            if doc["candidate_id"] != candidate_id:
                continue
            
            doc_tokens = doc["tokens"]
            intersection = query_tokens.intersection(doc_tokens)
            score = len(intersection) / (math.sqrt(len(query_tokens)) * math.sqrt(len(doc_tokens) + 1e-5))
            if score > 0.0:
                results.append((score, doc))

        results.sort(key=lambda x: x[0], reverse=True)
        return [{"content": doc["content"], "metadata": doc["metadata"], "score": round(score, 4)} for score, doc in results[:top_k]]


semantic_memory = SemanticVectorMemory()
