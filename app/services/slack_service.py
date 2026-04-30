
import json
import httpx

from app.core.config import settings
from app.models.call import BolnaCallPayload
from app.utils.formatter import build_slack_blocks
from app.utils.logger import logger


async def send_call_alert(call: BolnaCallPayload) -> None:
    """
    Build and POST a Slack alert for a completed Bolna call.

    Raises:
        httpx.HTTPStatusError: if Slack returns a non-2xx response.
    """
    blocks = build_slack_blocks(call)
    payload = {
        "text": f"Bolna call ended — ID: {call.id}",   # fallback / notification text
        "blocks": blocks,
    }

    logger.info("Sending Slack alert for call %s (agent %s)", call.id, call.agent_id)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            settings.slack_webhook_url,
            content=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

    logger.info("Slack alert sent successfully for call %s", call.id)