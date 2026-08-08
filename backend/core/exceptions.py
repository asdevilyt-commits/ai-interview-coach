class CareerAIException(Exception):
    """Base exception for Enterprise Career AI Platform."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AgentExecutionError(CareerAIException):
    """Raised when an autonomous sub-agent encounters an execution failure."""
    pass


class OrchestratorRoutingError(CareerAIException):
    """Raised when the Master Orchestrator fails to route intent or decompose task."""
    pass


class SkillExecutionError(CareerAIException):
    """Raised when a specialized skill fails to execute."""
    pass


class ToolExecutionError(CareerAIException):
    """Raised when an agent tool call fails."""
    pass


class MemoryError(CareerAIException):
    """Raised during operations on Structured, Vector, Graph, or Conversation memory layers."""
    pass


class RAGRetrievalError(CareerAIException):
    """Raised when RAG document indexing or retrieval encounters an issue."""
    pass


class CandidateDataIsolationError(CareerAIException):
    """Security exception raised when cross-candidate data leakage is attempted."""
    pass


class ModelInvocationError(CareerAIException):
    """Raised when LLM invocation or structured output generation fails."""
    pass
