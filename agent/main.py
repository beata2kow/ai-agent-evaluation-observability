from agent.models import (
    AgentRunResult,
    Scenario,
    StepResult,
)
from agent.tools import execute_tool
from observability.recorder import TraceRecorder

def run_scenario(
    scenario: Scenario,
    trace_recorder: TraceRecorder | None = None,
) -> AgentRunResult:
    """Execute a QA scenario and optionally record its observability trace."""
    step_results: list[StepResult] = []
    for step_number, step in enumerate(scenario.steps, start=1):
        started_counter = None
        if trace_recorder is not None:
            started_counter = trace_recorder.record_tool_started(
                step_number=step_number,
                tool_name=step.tool,
            )
        try:
            actual_result = execute_tool(
                tool_name=step.tool,
                parameters=step.parameters,
            )
        except Exception as error:
            if trace_recorder is not None and started_counter is not None:
                trace_recorder.record_tool_failed(
                    step_number=step_number,
                    tool_name=step.tool,
                    started_counter=started_counter,
                    error=error,
                )
            raise
        else:
            if trace_recorder is not None and started_counter is not None:
                trace_recorder.record_tool_completed(
                    step_number=step_number,
                    tool_name=step.tool,
                    started_counter=started_counter,
                )
        passed = actual_result == step.expected_result
        step_results.append(
            StepResult(
                description=step.description,
                tool=step.tool,
                actual_result=actual_result,
                expected_result=step.expected_result,
                passed=passed,
            )
        )

    total_steps = len(step_results)
    passed_steps = sum(
        1 for result in step_results if result.passed
    )
    failed_steps = total_steps - passed_steps
    status = "passed" if failed_steps == 0 else "failed"
    if trace_recorder is not None:
        trace_recorder.record_scenario_completed()
    return AgentRunResult(
        scenario_id=scenario.scenario_id,
        status=status,
        total_steps=total_steps,
        passed_steps=passed_steps,
        failed_steps=failed_steps,
        results=step_results,
    )
