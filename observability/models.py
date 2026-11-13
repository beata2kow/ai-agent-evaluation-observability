
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

EventType = Literal[
    "scenario.started",
    "tool.started",
    "tool.completed",
    "tool.failed",
    "scenario.completed",
]

class TraceEvent(BaseModel):
    """A single event recorded during agent execution."""
    event_id: str
    run_id: str
    scenario_id: str
    event_type: EventType
    timestamp: datetime
    step_number: int | None = Field(default=None, ge=1)
    tool_name: str | None = None
    duration_ms: float | None = Field(default=None, ge=0.0)
    status: Literal["success", "failure"] | None = None
    error_type: str | None = None
    error_message: str | None = None

class AgentTrace(BaseModel):
    """Complete execution trace for a single agent run."""
    run_id: str
    scenario_id: str
    started_at: datetime
    completed_at: datetime | None = None
    events: list[TraceEvent] = Field(default_factory=list)
