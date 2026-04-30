
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field


class TelephonyData(BaseModel):
    duration: Optional[float] = None          # call duration in seconds
    to_number: Optional[str] = None
    from_number: Optional[str] = None
    recording_url: Optional[str] = None
    call_type: Optional[str] = None           # "outbound" | "inbound"
    provider: Optional[str] = None            # "twilio" | "plivo" | ...
    hangup_by: Optional[str] = None
    hangup_reason: Optional[str] = None
    model_config = {"extra": "allow"}


class CostBreakdown(BaseModel):
    llm: Optional[float] = None
    network: Optional[float] = None
    platform: Optional[float] = None
    synthesizer: Optional[float] = None
    transcriber: Optional[float] = None
    model_config = {"extra": "allow"}


class BolnaCallPayload(BaseModel):
    """
    Bolna fires this payload to your webhook on every call status change.
    We act only when status == 'completed'.
    """
    id: str                                          # execution UUID
    agent_id: str                                    # agent UUID
    status: str                                      # scheduled → completed
    transcript: Optional[str] = None
    conversation_time: Optional[float] = None        # seconds (from Bolna)
    total_cost: Optional[float] = None               # in cents
    telephony_data: Optional[TelephonyData] = None
    cost_breakdown: Optional[CostBreakdown] = None
    answered_by_voice_mail: Optional[bool] = None
    error_message: Optional[str] = None
    extracted_data: Optional[dict[str, Any]] = None
    context_details: Optional[dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    model_config = {"extra": "allow"}

    @property
    def duration(self) -> float:
        """
        Best-effort duration in seconds.
        Prefers telephony_data.duration (actual call time),
        falls back to conversation_time (Bolna's own metric).
        """
        if self.telephony_data and self.telephony_data.duration is not None:
            return float(self.telephony_data.duration)
        return float(self.conversation_time or 0)

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"