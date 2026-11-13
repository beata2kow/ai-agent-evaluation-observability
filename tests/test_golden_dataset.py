import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from agent.models import GoldenDataset, GoldenScenario

DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "evaluations"
    / "golden_dataset.json"
)

def test_golden_dataset_loads_from_json():
    with DATASET_PATH.open(encoding="utf-8") as file:
        data = json.load(file)
    dataset = GoldenDataset.model_validate(data)
    assert dataset.dataset_name == "login_agent_golden_dataset"
    assert len(dataset.scenarios) == 3

def test_golden_scenario_accepts_valid_data():
    scenario = GoldenScenario(
        scenario_id="LOGIN-001",
        expected_agent_status="passed",
        expected_step_results=[True, True, True],
    )
    assert scenario.expected_agent_status == "passed"
    assert len(scenario.expected_step_results) == 3

def test_golden_scenario_rejects_invalid_status():
    with pytest.raises(ValidationError):
        GoldenScenario(
            scenario_id="LOGIN-001",
            expected_agent_status="unknown",
            expected_step_results=[True],
        )

def test_golden_scenario_rejects_empty_step_results():
    with pytest.raises(ValidationError):
        GoldenScenario(
            scenario_id="LOGIN-001",
            expected_agent_status="passed",
            expected_step_results=[],
        )

def test_golden_dataset_rejects_empty_scenarios():
    with pytest.raises(ValidationError):
        GoldenDataset(
            dataset_name="empty_dataset",
            dataset_version="1.0.0",
            description="Empty dataset",
            scenarios=[],
        )
