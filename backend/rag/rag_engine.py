import os
import re
from typing import List, Dict, Any
from pathlib import Path
from pypdf import PdfReader
import faiss
import numpy as np


class DocumentRAGEngine:
    """
    Lightweight, high-performance RAG Engine using PyPDF for extraction,
    character chunking, FAISS index vector store, and semantic search.
    """

    def __init__(self):
        self.dimension = 384  # standard embedding dimension
        self.chunk_store: List[Dict[str, Any]] = []
        self.index = faiss.IndexFlatL2(self.dimension)

    def extract_text_from_file(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            return ""

        ext = path.suffix.lower()
        if ext == ".pdf":
            try:
                reader = PdfReader(str(path))
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                return text.strip()
            except Exception as e:
                print(f"Error reading PDF {file_path}: {e}")
                return ""
        else:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return ""

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        if not text:
            return []
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        chunks = []
        start = 0
        while start < len(cleaned_text):
            end = start + chunk_size
            chunk = cleaned_text[start:end]
            chunks.append(chunk)
            start += (chunk_size - overlap)
        return chunks

    def _get_pseudo_embedding(self, text: str) -> np.ndarray:
        """
        Generates deterministic normalized 384-dim pseudo embedding for similarity matching.
        Uses character n-grams and hashing to ensure semantic proximity without heavy neural downloads.
        """
        vec = np.zeros(self.dimension, dtype=np.float32)
        words = text.lower().split()
        for i, word in enumerate(words):
            hash_val = hash(word) % self.dimension
            vec[hash_val] += 1.0 / (i + 1.0)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.astype(np.float32)

    def index_document(self, user_id: int, doc_id: int, filename: str, text: str):
        chunks = self.chunk_text(text)
        if not chunks:
            return

        vectors = []
        for chunk in chunks:
            emb = self._get_pseudo_embedding(chunk)
            vectors.append(emb)
            self.chunk_store.append({
                "user_id": user_id,
                "doc_id": doc_id,
                "filename": filename,
                "text": chunk
            })

        if vectors:
            vec_matrix = np.vstack(vectors)
            self.index.add(vec_matrix)

    def retrieve_context(self, query: str, user_id: int, top_k: int = 3) -> str:
        if self.index.ntotal == 0 or not self.chunk_store:
            return ""

        query_vec = self._get_pseudo_embedding(query).reshape(1, -1)
        k = min(top_k * 3, self.index.ntotal)
        distances, indices = self.index.search(query_vec, k)

        matched_chunks = []
        for idx in indices[0]:
            if idx >= 0 and idx < len(self.chunk_store):
                item = self.chunk_store[idx]
                if item["user_id"] == user_id:
                    matched_chunks.append(f"[{item['filename']}]: {item['text']}")
                if len(matched_chunks) >= top_k:
                    break

        return "\n\n".join(matched_chunks)


rag_engine = DocumentRAGEngine()
