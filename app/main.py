from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import httpx

# Load .env variables
load_dotenv()

# Get Slack webhook URL
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

app = FastAPI(title="Bolna → Slack Integration")


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/webhook/bolna")
async def bolna_webhook(request: Request):

    try:
        payload = await request.json()

        print("Received Payload:")
        print(payload)

        print("Webhook URL:", SLACK_WEBHOOK_URL)

        # Extract data from Bolna payload
        call_id = payload.get("id", "N/A")
        agent_id = payload.get("agent_id", "N/A")
        duration = payload.get("conversation_time", "N/A")
        transcript = payload.get(
            "transcript",
            "No transcript available"
        )

        # Slack message
        slack_payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📞 Bolna Call Ended"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Call ID:*\n{call_id}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Agent ID:*\n{agent_id}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Duration:*\n{duration} sec"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Transcript:*\n{transcript}"
                    }
                }
            ]
        }

        # Send to Slack
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SLACK_WEBHOOK_URL,
                json=slack_payload
            )

            print("Slack Status:", response.status_code)
            print("Slack Response:", response.text)

        return {
            "status": "success",
            "message": "Slack alert sent"
        }

    except Exception as e:
        print("ERROR:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }