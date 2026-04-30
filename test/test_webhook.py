
import json
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.call import BolnaCallPayload
from app.utils.formatter import format_duration, truncate, build_slack_blocks


# ── format_duration ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("seconds,expected", [
    (0,     "0s"),
    (45,    "45s"),
    (59.9,  "1m"),
    (120,   "2m"),
    (125,   "2m 5s"),
])
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected


# ── truncate ──────────────────────────────────────────────────────────────────

def test_truncate_short():
    assert truncate("hello", 20) == "hello"

def test_truncate_long():
    assert truncate("hello world!", 8) == "hello..."


# ── BolnaCallPayload model ────────────────────────────────────────────────────

def _make_payload(**overrides) -> BolnaCallPayload:
    base = {
        "id": "exec-001",
        "agent_id": "agent-abc",
        "status": "completed",
        "transcript": "User: Hi\nAgent: Hello!",
        "conversation_time": 95.0,
        "telephony_data": {
            "duration": 90.0,
            "to_number": "+911234567890",
            "from_number": "+919876543210",
            "call_type": "outbound",
            "hangup_by": "Caller",
        },
    }
    base.update(overrides)
    return BolnaCallPayload(**base)


def test_payload_duration_prefers_telephony():
    call = _make_payload()
    assert call.duration == 90.0   # telephony_data.duration


def test_payload_duration_falls_back_to_conversation_time():
    call = _make_payload(telephony_data=None, conversation_time=77.0)
    assert call.duration == 77.0


def test_payload_is_completed_true():
    assert _make_payload(status="completed").is_completed is True

def test_payload_is_completed_false():
    assert _make_payload(status="in-progress").is_completed is False


# ── build_slack_blocks ────────────────────────────────────────────────────────

def test_build_slack_blocks_contains_required_fields():
    call = _make_payload()
    blocks = build_slack_blocks(call)
    raw = json.dumps(blocks)

    assert "exec-001" in raw
    assert "agent-abc" in raw
    assert "1m 30s" in raw          # 90s duration
    assert "User: Hi" in raw

    types = [b["type"] for b in blocks]
    assert "header" in types
    assert "divider" in types
    assert "context" in types


def test_build_slack_blocks_no_telephony():
    call = _make_payload(telephony_data=None, conversation_time=30.0)
    blocks = build_slack_blocks(call)
    # Should still build without errors
    assert len(blocks) >= 4


# ── Webhook endpoint (integration) ────────────────────────────────────────────

COMPLETED_PAYLOAD = {
    "id": "exec-999",
    "agent_id": "agent-xyz",
    "status": "completed",
    "transcript": "User: Test call\nAgent: Got it!",
    "conversation_time": 42.0,
}

IN_PROGRESS_PAYLOAD = {
    "id": "exec-888",
    "agent_id": "agent-xyz",
    "status": "in-progress",
    "transcript": None,
    "conversation_time": 0,
}


@pytest.mark.asyncio
async def test_webhook_completed_sends_slack():
    mock_slack = AsyncMock()
    with patch("app.services.bolna_service.send_call_alert", mock_slack):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/webhook/bolna", json=COMPLETED_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["action"] == "alerted"
    mock_slack.assert_awaited_once()


@pytest.mark.asyncio
async def test_webhook_in_progress_skips_slack():
    mock_slack = AsyncMock()
    with patch("app.services.bolna_service.send_call_alert", mock_slack):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/webhook/bolna", json=IN_PROGRESS_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["action"] == "skipped"
    mock_slack.assert_not_awaited()


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"