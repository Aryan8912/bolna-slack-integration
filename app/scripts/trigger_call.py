
import argparse
import asyncio
import json
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from app.core.config import settings
from app.utils.logger import logger

MAKE_CALL_URL = f"{settings.bolna_base_url}/call"


async def trigger_call(to_number: str, webhook_url: str) -> None:
    if not settings.bolna_api_key:
        logger.error("BOLNA_API_KEY is not set in .env")
        sys.exit(1)
    if not settings.bolna_agent_id:
        logger.error("BOLNA_AGENT_ID is not set in .env")
        sys.exit(1)

    payload = {
        "agent_id": settings.bolna_agent_id,
        "recipient_phone_number": to_number,
        "user_data": "test-call-from-script",
        "webhook_url": webhook_url,
    }

    logger.info("Triggering Bolna call to %s ...", to_number)

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            MAKE_CALL_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.bolna_api_key}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        data = response.json()

    execution_id = data.get("execution_id", "(unknown)")
    logger.info("Call triggered! Execution ID: %s", execution_id)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger a Bolna outbound call")
    parser.add_argument("--to", required=True, help="Recipient phone number (E.164 format)")
    parser.add_argument(
        "--webhook",
        default="http://localhost:8000/webhook/bolna",
        help="Webhook URL for Bolna to POST call updates to",
    )
    args = parser.parse_args()
    asyncio.run(trigger_call(args.to, args.webhook))