from agent.models import (
    AgentRunResult,
    Scenario,
    StepResult,
)
from agent.tools import execute_tool

def run_scenario(scenario: Scenario) -> AgentRunResult:
    """Execute all steps defined in a QA scenario and return a structured execution report."""

    step_results: list[StepResult] = []

    for step in scenario.steps:
        actual_result = execute_tool(
            tool_name=step.tool,
            parameters=step.parameters,
        )
        passed = actual_result == step.expected_result
        step_result = StepResult(
            description=step.description,
            tool=step.tool,
            actual_result=actual_result,
            expected_result=step.expected_result,
            passed=passed,
        )
        step_results.append(step_result)

    total_steps = len(step_results)
    passed_steps = sum(
        1 for result in step_results if result.passed
    )
    failed_steps = total_steps - passed_steps

    status = "passed" if failed_steps == 0 else "failed"

    return AgentRunResult(
        scenario_id=scenario.scenario_id,
        status=status,
        total_steps=total_steps,
        passed_steps=passed_steps,
        failed_steps=failed_steps,
        results=step_results,
    )