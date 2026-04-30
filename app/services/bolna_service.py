
from app.models.call import BolnaCallPayload
from app.services.slack_service import send_call_alert
from app.utils.logger import logger


async def process_bolna_event(payload: BolnaCallPayload) -> dict:
    """
    Entry point called by the webhook route.

    Bolna sends status updates at every stage:
        scheduled → queued → initiated → in-progress → completed

    We only alert on 'completed' (when transcript is fully available).

    Returns a dict describing what action was taken.
    """
    logger.info(
        "Received Bolna event | call=%s | agent=%s | status=%s",
        payload.id,
        payload.agent_id,
        payload.status,
    )

    if not payload.is_completed:
        logger.debug("Skipping non-completed status: %s", payload.status)
        return {"action": "skipped", "reason": f"status is '{payload.status}', not 'completed'"}

    if not payload.transcript:
        logger.warning("Call %s completed but transcript is empty", payload.id)

    await send_call_alert(payload)

    return {
        "action": "alerted",
        "call_id": payload.id,
        "agent_id": payload.agent_id,
        "duration": payload.duration,
    }