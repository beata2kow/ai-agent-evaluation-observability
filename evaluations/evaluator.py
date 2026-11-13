
from agent.models import AgentRunResult, GoldenDataset
from evaluations.models import EvaluationReport, ScenarioEvaluation


def evaluate_dataset(
    agent_results: list[AgentRunResult],
    golden_dataset: GoldenDataset,
) -> EvaluationReport:
    """Evaluate agent execution results against a golden dataset."""

    result_ids = [result.scenario_id for result in agent_results]
    golden_ids = [scenario.scenario_id for scenario in golden_dataset.scenarios]

    if len(result_ids) != len(set(result_ids)):
        raise ValueError("Duplicate scenario IDs in agent results.")

    if len(golden_ids) != len(set(golden_ids)):
        raise ValueError("Duplicate scenario IDs in golden dataset.")

    missing_ids = set(golden_ids) - set(result_ids)
    unexpected_ids = set(result_ids) - set(golden_ids)

    if missing_ids:
        raise ValueError(f"Missing agent results for scenarios: {sorted(missing_ids)}")

    if unexpected_ids:
        raise ValueError(f"Unexpected agent results for scenarios: {sorted(unexpected_ids)}")

    results_by_id = {
        result.scenario_id: result
        for result in agent_results
    }

    scenario_evaluations = []

    for golden_scenario in golden_dataset.scenarios:
        agent_result = results_by_id[golden_scenario.scenario_id]

        expected_steps = golden_scenario.expected_step_results
        actual_steps = agent_result.results

        if len(actual_steps) != len(expected_steps):
            raise ValueError(
                f"Step count mismatch for scenario "
                f"{golden_scenario.scenario_id}: "
                f"expected {len(expected_steps)}, got {len(actual_steps)}."
            )

        correct_steps = sum(
            actual.actual_result == expected
            for actual, expected in zip(actual_steps, expected_steps)
        )

        total_steps = len(expected_steps)
        step_accuracy = correct_steps / total_steps

        status_matches = (
            agent_result.status == golden_scenario.expected_agent_status
        )

        task_completed = correct_steps == total_steps

        scenario_evaluations.append(
            ScenarioEvaluation(
                scenario_id=golden_scenario.scenario_id,
                expected_status=golden_scenario.expected_agent_status,
                actual_status=agent_result.status,
                status_matches=status_matches,
                task_completed=task_completed,
                total_steps=total_steps,
                correct_steps=correct_steps,
                step_accuracy=step_accuracy,
            )
        )

    total_scenarios = len(scenario_evaluations)
    completed_scenarios = sum(
        result.task_completed
        for result in scenario_evaluations
    )

    total_steps = sum(
        result.total_steps
        for result in scenario_evaluations
    )

    correct_steps = sum(
        result.correct_steps
        for result in scenario_evaluations
    )

    return EvaluationReport(
        dataset_name=golden_dataset.dataset_name,
        dataset_version=golden_dataset.dataset_version,
        total_scenarios=total_scenarios,
        completed_scenarios=completed_scenarios,
        task_completion_rate=completed_scenarios / total_scenarios,
        total_steps=total_steps,
        correct_steps=correct_steps,
        step_accuracy=correct_steps / total_steps,
        scenario_results=scenario_evaluations,
    )
