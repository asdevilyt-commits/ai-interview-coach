from typing import Dict, Any, Optional, List
from backend.memory.structured_memory import structured_memory, StructuredMemory
from backend.memory.semantic_memory import semantic_memory, SemanticVectorMemory
from backend.memory.knowledge_graph import knowledge_graph_memory, KnowledgeGraphMemory
from backend.memory.conversation_memory import conversation_memory, ConversationMemory
from backend.models.candidate import CandidateProfile


class HybridMemory:
    """
    Unified Enterprise Hybrid Memory Manager across 4 Tiers:
    1. Structured Memory (PostgreSQL / Models)
    2. Semantic Vector Memory (FAISS / Vector Index)
    3. Knowledge Graph Memory (Relationships)
    4. Conversation Memory (Redis / Checkpoints)
    """
    def __init__(self):
        self.structured = structured_memory
        self.semantic = semantic_memory
        self.graph = knowledge_graph_memory
        self.conversation = conversation_memory

    def sync_candidate_state(self, profile: CandidateProfile):
        self.structured.save_candidate(profile)
        self.graph.sync_candidate_profile(profile.candidate_id, profile.model_dump(mode="json"))

    def get_candidate_full_context(self, candidate_id: str, query: Optional[str] = None) -> Dict[str, Any]:
        profile = self.structured.get_candidate(candidate_id)
        graph_subgraph = self.graph.get_candidate_subgraph(candidate_id)
        vector_results = self.semantic.search(candidate_id, query, top_k=3) if query else []
        
        return {
            "profile": profile.model_dump(mode="json") if profile else {},
            "knowledge_graph": graph_subgraph,
            "semantic_notes": vector_results,
        }


hybrid_memory = HybridMemory()
