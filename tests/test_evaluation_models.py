
import pytest
from pydantic import ValidationError
from evaluations.models import EvaluationReport, ScenarioEvaluation

def test_valid_scenario_evaluation():
    result = ScenarioEvaluation(
        scenario_id="LOGIN-001",
        expected_status="passed",
        actual_status="passed",
        status_matches=True,
        task_completed=True,
        total_steps=3,
        correct_steps=3,
        step_accuracy=1.0,
    )
    assert result.task_completed is True
    assert result.step_accuracy == 1.0

def test_scenario_evaluation_rejects_invalid_status():
    with pytest.raises(ValidationError):
        ScenarioEvaluation(
            scenario_id="LOGIN-001",
            expected_status="unknown",
            actual_status="passed",
            status_matches=False,
            task_completed=False,
            total_steps=3,
            correct_steps=2,
            step_accuracy=2 / 3,
        )

def test_scenario_evaluation_rejects_invalid_accuracy():
    with pytest.raises(ValidationError):
        ScenarioEvaluation(
            scenario_id="LOGIN-001",
            expected_status="passed",
            actual_status="passed",
            status_matches=True,
            task_completed=True,
            total_steps=3,
            correct_steps=3,
            step_accuracy=1.5,
        )

def test_valid_evaluation_report():
    report = EvaluationReport(
        dataset_name="login_agent_golden_dataset",
        dataset_version="1.0.0",
        total_scenarios=1,
        completed_scenarios=1,
        task_completion_rate=1.0,
        total_steps=3,
        correct_steps=3,
        step_accuracy=1.0,
        scenario_results=[
            ScenarioEvaluation(
                scenario_id="LOGIN-001",
                expected_status="passed",
                actual_status="passed",
                status_matches=True,
                task_completed=True,
                total_steps=3,
                correct_steps=3,
                step_accuracy=1.0,
            )
        ],
    )
    assert report.total_scenarios == 1
    assert report.task_completion_rate == 1.0
