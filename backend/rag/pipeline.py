from typing import List, Dict, Any, Optional
from backend.memory.semantic_memory import semantic_memory
from backend.core.logger import logger


class RAGPipeline:
    """
    RAG System for Interview & Candidate Knowledge.
    Pipeline: Text Extraction -> Chunking -> Embedding -> Vector DB -> Retriever -> Candidate Isolation -> Context
    """
    def __init__(self):
        self.chunk_size = 500
        self.chunk_overlap = 50

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i : i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        return chunks or [text]

    def index_document(
        self,
        candidate_id: str,
        document_text: str,
        doc_type: str = "resume",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        chunks = self.chunk_text(document_text)
        meta = metadata or {}
        meta["doc_type"] = doc_type

        for idx, chunk in enumerate(chunks):
            chunk_meta = {**meta, "chunk_index": idx}
            semantic_memory.add_document(candidate_id=candidate_id, content=chunk, metadata=chunk_meta)

        logger.info(f"Indexed document for candidate '{candidate_id}' into RAG ({len(chunks)} chunks).")
        return len(chunks)

    def retrieve(self, candidate_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retriever with Candidate-level Data Isolation.
        Guarantees candidate A can NEVER retrieve candidate B's indexed docs.
        """
        return semantic_memory.search(candidate_id=candidate_id, query=query, top_k=top_k)


rag_pipeline = RAGPipeline()
