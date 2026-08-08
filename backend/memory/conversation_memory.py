from typing import Dict, List, Any, Optional
from backend.core.logger import logger


class ConversationMemory:
    """
    Tier 4 — Conversation Memory.
    Manages active state sessions, thread history, and LangGraph checkpoints.
    """
    def __init__(self):
        self._sessions: Dict[str, List[Dict[str, Any]]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append({
            "role": role,
            "content": content,
        })
        logger.info(f"Added '{role}' message to session '{session_id}'. Total messages: {len(self._sessions[session_id])}")

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self._sessions.get(session_id, [])

    def clear_history(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]


conversation_memory = ConversationMemory()
