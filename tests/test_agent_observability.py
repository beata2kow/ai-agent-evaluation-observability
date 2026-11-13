import pytest
from agent.main import run_scenario
from agent.models import Scenario
from observability.recorder import TraceRecorder

def create_scenario() -> Scenario:
    return Scenario(
        scenario_id="LOGIN-TEST",
        title="Observability integration test",
        steps=[
            {
                "description": "Check whether the user exists",
                "tool": "check_user_exists",
                "parameters": {"username": "qa_user"},
                "expected_result": True,
            }
        ],
    )

def test_run_scenario_records_successful_execution():
    scenario = create_scenario()
    recorder = TraceRecorder(scenario.scenario_id)
    result = run_scenario(
        scenario,
        trace_recorder=recorder,
    )
    trace = recorder.get_trace()
    assert result.status == "passed"
    assert [event.event_type for event in trace.events] == [
        "scenario.started",
        "tool.started",
        "tool.completed",
        "scenario.completed",
    ]
    assert trace.completed_at is not None
    assert trace.events[2].status == "success"
    assert trace.events[2].duration_ms >= 0

def test_run_scenario_records_tool_failure(monkeypatch):
    scenario = create_scenario()
    recorder = TraceRecorder(scenario.scenario_id)
    def failing_tool(*args, **kwargs):
        raise ValueError("Simulated tool failure")
    monkeypatch.setattr("agent.main.execute_tool", failing_tool)
    with pytest.raises(ValueError, match="Simulated tool failure"):
        run_scenario(
            scenario,
            trace_recorder=recorder,
        )
    trace = recorder.get_trace()
    assert [event.event_type for event in trace.events] == [
        "scenario.started",
        "tool.started",
        "tool.failed",
    ]
    failed_event = trace.events[-1]
    assert failed_event.status == "failure"
    assert failed_event.error_type == "ValueError"
    assert failed_event.error_message == "Simulated tool failure"
    assert failed_event.duration_ms >= 0
    assert trace.completed_at is None
