from fastapi import FastAPI
import logging
from app.config import get_settings
from app.core.logging import configure_logging
from app.api.tickets import router as tickets_router

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title = settings.app_name,
            version = settings.app_version
            )

app.include_router(tickets_router)

@app.get("/health", tags=['Health'])
def health_check() -> dict[str,str]:
    '''return the appllication's basic health status.'''
    logger.info("Health check requested")
    return {"status": "Healthy"}
