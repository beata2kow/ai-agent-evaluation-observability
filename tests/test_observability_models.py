from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from observability.models import AgentTrace, TraceEvent

@pytest.fixture
def sample_event():
    return TraceEvent(
        event_id="event-001",
        run_id="run-001",
        scenario_id="LOGIN-001",
        event_type="tool.completed",
        timestamp=datetime.now(timezone.utc),
        step_number=1,
        tool_name="check_user_exists",
        duration_ms=2.45,
        status="success",
    )

def test_valid_trace_event(sample_event):
    assert sample_event.event_type == "tool.completed"
    assert sample_event.step_number == 1
    assert sample_event.duration_ms == 2.45
    assert sample_event.status == "success"

def test_trace_event_rejects_invalid_event_type():
    with pytest.raises(ValidationError):
        TraceEvent(
            event_id="event-002",
            run_id="run-001",
            scenario_id="LOGIN-001",
            event_type="invalid.event",
            timestamp=datetime.now(timezone.utc),
        )

def test_trace_event_rejects_negative_duration():
    with pytest.raises(ValidationError):
        TraceEvent(
            event_id="event-003",
            run_id="run-001",
            scenario_id="LOGIN-001",
            event_type="tool.completed",
            timestamp=datetime.now(timezone.utc),
            duration_ms=-1.0,
        )

def test_valid_agent_trace(sample_event):
    trace = AgentTrace(
        run_id="run-001",
        scenario_id="LOGIN-001",
        started_at=datetime.now(timezone.utc),
        events=[sample_event],
    )
    assert trace.run_id == "run-001"
    assert len(trace.events) == 1
    assert trace.completed_at is None

def test_agent_trace_can_be_created_without_events():
    trace = AgentTrace(
        run_id="run-002",
        scenario_id="LOGIN-002",
        started_at=datetime.now(timezone.utc),
    )
    assert trace.events == []
