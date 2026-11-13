import pytest
from observability.recorder import TraceRecorder

def test_recorder_creates_trace_with_unique_run_id():
    recorder_1 = TraceRecorder("LOGIN-001")
    recorder_2 = TraceRecorder("LOGIN-001")
    trace_1 = recorder_1.get_trace()
    trace_2 = recorder_2.get_trace()
    assert trace_1.run_id != trace_2.run_id
    assert trace_1.scenario_id == "LOGIN-001"

def test_recorder_records_scenario_started():
    recorder = TraceRecorder("LOGIN-001")
    trace = recorder.get_trace()
    assert len(trace.events) == 1
    assert trace.events[0].event_type == "scenario.started"
    assert trace.events[0].run_id == trace.run_id

def test_recorder_records_successful_tool_execution():
    recorder = TraceRecorder("LOGIN-001")
    started_counter = recorder.record_tool_started(
        step_number=1,
        tool_name="check_user_exists",
    )
    recorder.record_tool_completed(
        step_number=1,
        tool_name="check_user_exists",
        started_counter=started_counter,
    )
    events = recorder.get_trace().events
    assert events[1].event_type == "tool.started"
    assert events[2].event_type == "tool.completed"
    assert events[2].status == "success"
    assert events[2].duration_ms >= 0
    assert events[2].step_number == 1

def test_recorder_records_tool_failure():
    recorder = TraceRecorder("LOGIN-001")
    started_counter = recorder.record_tool_started(
        step_number=1,
        tool_name="check_user_exists",
    )
    error = ValueError("Missing username")
    recorder.record_tool_failed(
        step_number=1,
        tool_name="check_user_exists",
        started_counter=started_counter,
        error=error,
    )
    failed_event = recorder.get_trace().events[-1]
    assert failed_event.event_type == "tool.failed"
    assert failed_event.status == "failure"
    assert failed_event.error_type == "ValueError"
    assert failed_event.error_message == "Missing username"
    assert failed_event.duration_ms >= 0

def test_recorder_records_scenario_completion():
    recorder = TraceRecorder("LOGIN-001")
    recorder.record_scenario_completed()
    trace = recorder.get_trace()
    assert trace.completed_at is not None
    assert trace.events[-1].event_type == "scenario.completed"

def test_all_events_share_the_same_run_id():
    recorder = TraceRecorder("LOGIN-001")
    started_counter = recorder.record_tool_started(
        step_number=1,
        tool_name="check_user_exists",
    )
    recorder.record_tool_completed(
        step_number=1,
        tool_name="check_user_exists",
        started_counter=started_counter,
    )
    trace = recorder.get_trace()
    assert all(
        event.run_id == trace.run_id
        for event in trace.events
    )
