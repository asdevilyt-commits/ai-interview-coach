FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn pydantic-settings langchain-core langchain-groq langgraph pydantic python-dotenv asyncpg redis

COPY backend/ backend/

EXPOSE 8000

CMD ["uvicorn", "backend.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
