
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.models.call import BolnaCallPayload
from app.services.bolna_service import process_bolna_event
from app.utils.logger import logger

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/bolna")
async def bolna_webhook(payload: BolnaCallPayload, request: Request):
    """
    Receives Bolna call status updates and sends a Slack alert
    when the call is completed.
    """
    try:
        result = await process_bolna_event(payload)
        return JSONResponse(status_code=200, content={"ok": True, **result})

    except Exception as exc:
        logger.exception("Unhandled error processing Bolna webhook: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error") from exc