"""
app/utils/formatter.py

Builds the Slack Block Kit payload for a completed Bolna call.
"""

from __future__ import annotations
import math
from datetime import datetime, timezone
from app.models.call import BolnaCallPayload

TRANSCRIPT_LIMIT = 2_800   # Slack block text hard cap ~3 000 chars


def format_duration(seconds: float) -> str:
    """45 → '45s' | 125 → '2m 5s'"""
    total = math.floor(seconds + 0.5)
    mins, secs = divmod(total, 60)
    if mins == 0:
        return f"{total}s"
    return f"{mins}m" if secs == 0 else f"{mins}m {secs}s"


def truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def build_slack_blocks(call: BolnaCallPayload) -> list[dict]:
    """Return a Slack Block Kit blocks array for a completed call."""

    ts = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    duration_str = format_duration(call.duration)
    transcript_text = truncate(call.transcript or "(no transcript)", TRANSCRIPT_LIMIT)

    # Status emoji
    status_emoji = "✅" if call.is_completed else "⚠️"

    blocks: list[dict] = [
        # ── Header ────────────────────────────────────────────────────────
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{status_emoji} Bolna Call Ended",
                "emoji": True,
            },
        },
        # ── Metadata grid ─────────────────────────────────────────────────
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Call ID*\n`{call.id}`"},
                {"type": "mrkdwn", "text": f"*Agent ID*\n`{call.agent_id}`"},
                {"type": "mrkdwn", "text": f"*Duration*\n{duration_str}"},
                {"type": "mrkdwn", "text": f"*Status*\n`{call.status}`"},
            ],
        },
    ]

    # ── Optional telephony details ─────────────────────────────────────────
    td = call.telephony_data
    if td and (td.to_number or td.from_number):
        blocks.append({
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*From*\n{td.from_number or '—'}"},
                {"type": "mrkdwn", "text": f"*To*\n{td.to_number or '—'}"},
                {"type": "mrkdwn", "text": f"*Call type*\n{td.call_type or '—'}"},
                {"type": "mrkdwn", "text": f"*Hangup by*\n{td.hangup_by or '—'}"},
            ],
        })

    blocks.append({"type": "divider"})

    # ── Transcript ─────────────────────────────────────────────────────────
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Transcript*\n```{transcript_text}```",
        },
    })

    # ── Footer ─────────────────────────────────────────────────────────────
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": (
                    f"🕐 {ts}  ·  "
                    "Sent by *bolna-slack-integration*  ·  "
                    "<https://platform.bolna.ai|Bolna Dashboard>"
                ),
            }
        ],
    })

    return blocks