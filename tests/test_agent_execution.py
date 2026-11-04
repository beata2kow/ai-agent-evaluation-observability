from agent.main import run_scenario
from agent.models import Scenario, ScenarioStep

def test_successful_scenario():
    scenario = Scenario(
        scenario_id="LOGIN-001",
        title="Successful login",
        steps=[
            ScenarioStep(
                description="Check user",
                tool="check_user_exists",
                parameters={"username": "qa_user"},
                expected_result=True,
            ),
            ScenarioStep(
                description="Validate credentials",
                tool="validate_credentials",
                parameters={
                    "username": "qa_user",
                    "password": "correct_password",
                },
                expected_result=True,
            ),
        ],
    )
    result = run_scenario(scenario)
    assert result.status == "passed"
    assert result.total_steps == 2
    assert result.passed_steps == 2
    assert result.failed_steps == 0

def test_expected_negative_result_is_a_pass():
    scenario = Scenario(
        scenario_id="LOGIN-002",
        title="Unknown user is rejected",
        steps=[
            ScenarioStep(
                description="Check unknown user",
                tool="check_user_exists",
                parameters={"username": "unknown_user"},
                expected_result=False,
            ),
        ],
    )
    result = run_scenario(scenario)
    assert result.status == "passed"
    assert result.results[0].actual_result is False
    assert result.results[0].passed is True

def test_scenario_fails_when_expectation_is_not_met():
    scenario = Scenario(
        scenario_id="LOGIN-003",
        title="Incorrect expectation",
        steps=[
            ScenarioStep(
                description="Check user",
                tool="check_user_exists",
                parameters={"username": "unknown_user"},
                expected_result=True,
            ),
        ],
    )
    result = run_scenario(scenario)
    assert result.status == "failed"
    assert result.total_steps == 1
    assert result.passed_steps == 0
    assert result.failed_steps == 1

def test_scenario_returns_results_for_all_steps():
    scenario = Scenario(
        scenario_id="LOGIN-004",
        title="Multiple steps",
        steps=[
            ScenarioStep(
                description="Check first user",
                tool="check_user_exists",
                parameters={"username": "qa_user"},
                expected_result=True,
            ),
            ScenarioStep(
                description="Check second user",
                tool="check_user_exists",
                parameters={"username": "restricted_user"},
                expected_result=True,
            ),
            ScenarioStep(
                description="Check unknown user",
                tool="check_user_exists",
                parameters={"username": "unknown_user"},
                expected_result=False,
            ),
        ],
    )
    result = run_scenario(scenario)
    assert len(result.results) == 3
    assert result.passed_steps == 3
    assert result.status == "passed"