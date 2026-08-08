import time
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.core.logger import logger
from backend.database.connection import init_db
from backend.api.routes import router as api_router

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

# Initialize SQLite database models
init_db()

app = FastAPI(
    title="Simple AI Interview Coach",
    version="1.0.0",
    description="Personal AI Tuition Teacher / Mentor Capstone Application",
    debug=True,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} -> Status {response.status_code} ({duration:.3f}s)")
    return response


# Include API Router at root so /register, /profile, /dashboard etc work directly
app.include_router(api_router)
app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": "Simple AI Interview Coach",
        "version": "1.0.0"
    }


# Serve static frontend dashboard
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
