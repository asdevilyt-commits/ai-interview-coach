import os
from typing import Any, List, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from backend.config import settings
from backend.core.logger import logger
from backend.core.exceptions import ModelInvocationError


def get_llm(
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> ChatGroq:
    """
    Get configured ChatGroq instance.
    """
    api_key = settings.GROQ_API_KEY
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY", "")

    if not api_key:
        raise ModelInvocationError("GROQ_API_KEY is not set in environment or settings.")

    selected_model = model_name or settings.PRIMARY_LLM_MODEL
    selected_temp = temperature if temperature is not None else settings.LLM_TEMPERATURE
    selected_tokens = max_tokens or settings.LLM_MAX_TOKENS

    try:
        return ChatGroq(
            model=selected_model,
            temperature=selected_temp,
            max_tokens=selected_tokens,
            api_key=api_key,
        )
    except Exception as e:
        logger.error(f"Failed to initialize ChatGroq model ({selected_model}): {e}")
        raise ModelInvocationError(f"Initialization failure: {str(e)}") from e


def ask_llm(prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.0) -> str:
    """
    Convenience function to invoke LLM with simple text string and automatic fallback logic.
    """
    messages: List[BaseMessage] = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=prompt))

    # Try primary model
    try:
        llm = get_llm(model_name=settings.PRIMARY_LLM_MODEL, temperature=temperature)
        response = llm.invoke(messages)
        return str(response.content)
    except Exception as e:
        logger.warning(f"Primary model ({settings.PRIMARY_LLM_MODEL}) failed: {e}. Trying fallback model ({settings.FALLBACK_LLM_MODEL})...")
        try:
            fallback_llm = get_llm(model_name=settings.FALLBACK_LLM_MODEL, temperature=temperature)
            response = fallback_llm.invoke(messages)
            return str(response.content)
        except Exception as fallback_err:
            logger.error(f"Fallback model failed: {fallback_err}")
            raise ModelInvocationError(f"LLM execution failed on both primary and fallback models: {str(fallback_err)}") from fallback_err