
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routes.webhook import router as webhook_router
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Bolna-Slack integration started | env=%s | endpoint=POST /webhook/bolna",
        settings.app_env,
    )
    yield


app = FastAPI(
    title="Bolna → Slack Integration",
    description="Sends a Slack alert whenever a Bolna voice call ends.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(webhook_router)


@app.get("/health", tags=["Health"])
async def health():
    return JSONResponse({"status": "ok", "env": settings.app_env})