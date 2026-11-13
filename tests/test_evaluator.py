import json
from pathlib import Path
import pytest
from agent.models import AgentRunResult, StepResult, GoldenDataset
from evaluations.evaluator import evaluate_dataset

DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "evaluations"
    / "golden_dataset.json"
)

@pytest.fixture
def golden_dataset():
    with DATASET_PATH.open(encoding="utf-8") as file:
        data = json.load(file)
    return GoldenDataset.model_validate(data)

def build_agent_results(golden_dataset, overrides=None):
    """Build synthetic agent results based on golden expectations."""
    overrides = overrides or {}
    results = []

    for scenario in golden_dataset.scenarios:
        actual_values = list(
            overrides.get(
                scenario.scenario_id,
                scenario.expected_step_results,
            )
        )
        expected_values = scenario.expected_step_results
        step_results = [
            StepResult(
                description=f"Step {index + 1}",
                tool="check_user_exists",
                actual_result=actual,
                expected_result=expected,
                passed=actual == expected,
            )
            for index, (actual, expected) in enumerate(
                zip(actual_values, expected_values)
            )
        ]
        failed_steps = sum(
            not result.passed for result in step_results
        )
        results.append(
            AgentRunResult(
                scenario_id=scenario.scenario_id,
                status="failed" if failed_steps else "passed",
                total_steps=len(step_results),
                passed_steps=len(step_results) - failed_steps,
                failed_steps=failed_steps,
                results=step_results,
            )
        )
    return results

def test_evaluate_perfect_agent_execution(golden_dataset):
    agent_results = build_agent_results(golden_dataset)
    report = evaluate_dataset(agent_results, golden_dataset)
    assert report.total_scenarios == 3
    assert report.completed_scenarios == 3
    assert report.task_completion_rate == 1.0
    assert report.total_steps == 8
    assert report.correct_steps == 8
    assert report.step_accuracy == 1.0


def test_evaluate_partial_agent_failure(golden_dataset):
    agent_results = build_agent_results(
        golden_dataset,
        overrides={"LOGIN-001": [True, True, False]},
    )
    report = evaluate_dataset(agent_results, golden_dataset)
    assert report.completed_scenarios == 2
    assert report.task_completion_rate == pytest.approx(2 / 3)
    assert report.correct_steps == 7
    assert report.step_accuracy == pytest.approx(7 / 8)

def test_evaluator_rejects_missing_scenario_results(golden_dataset):
    agent_results = build_agent_results(golden_dataset)
    agent_results.pop()
    with pytest.raises(ValueError, match="Missing agent results"):
        evaluate_dataset(agent_results, golden_dataset)

def test_evaluator_rejects_unexpected_scenario_results(golden_dataset):
    agent_results = build_agent_results(golden_dataset)
    extra_result = agent_results[0].model_copy(
        update={"scenario_id": "LOGIN-999"}
    )
    agent_results.append(extra_result)
    with pytest.raises(ValueError, match="Unexpected agent results"):
        evaluate_dataset(agent_results, golden_dataset)

def test_evaluator_rejects_duplicate_agent_results(golden_dataset):
    agent_results = build_agent_results(golden_dataset)
    agent_results.append(agent_results[0])
    with pytest.raises(ValueError, match="Duplicate scenario IDs"):
        evaluate_dataset(agent_results, golden_dataset)

def test_evaluator_rejects_step_count_mismatch(golden_dataset):
    agent_results = build_agent_results(golden_dataset)
    agent_results[0].results.pop()
    with pytest.raises(ValueError, match="Step count mismatch"):
        evaluate_dataset(agent_results, golden_dataset)

def test_task_completion_is_independent_of_agent_status(golden_dataset):
    agent_results = build_agent_results(golden_dataset)
    # Simulate an incorrect status reported by the agent.
    # Actual step results still match the Golden Dataset.
    agent_results[0] = agent_results[0].model_copy(
        update={"status": "failed"}
    )
    report = evaluate_dataset(agent_results, golden_dataset)
    login_001 = next(
        result
        for result in report.scenario_results
        if result.scenario_id == "LOGIN-001"
    )
    assert login_001.status_matches is False
    assert login_001.task_completed is True
    assert report.completed_scenarios == 3
    assert report.task_completion_rate == 1.0