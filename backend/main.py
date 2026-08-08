import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from backend.config import settings
from backend.core.logger import logger



def main():
    logger.info(f"Starting {settings.APP_NAME} (v{settings.APP_VERSION}) on port 8000...")
    uvicorn.run(
        "backend.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()