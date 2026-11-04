import pytest
from pydantic import ValidationError
from agent.models import Scenario, ScenarioStep

def test_valid_test_case():
    case = Scenario(
        scenario_id="LOGIN-001",
        title="Successful login",
        steps=[
            ScenarioStep(
                description="Check whether user exists",
                tool="check_user_exists",
                parameters={"username": "test_user"},
                expected_result=True,
            )
        ],
    )
    assert case.scenario_id == "LOGIN-001"
    assert len(case.steps) == 1

def test_invalid_tool_is_rejected():
    with pytest.raises(ValidationError):
        ScenarioStep(
            description="Unknown operation",
            tool="delete_database",
            parameters={},
            expected_result=True,
        )

def test_scenario_requires_at_least_one_step():
    with pytest.raises(ValidationError):
        Scenario(
            scenario_id="LOGIN-002",
            title="Empty scenario",
            steps=[],
        )
