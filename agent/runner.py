import json
from pathlib import Path
from agent.main import run_scenario
from agent.models import Scenario

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_scenarios() -> list[Scenario]:
    """Load and validate scenarios from the JSON dataset."""
    dataset_path = PROJECT_ROOT / "datasets" / "login_scenarios.json"
    with dataset_path.open(encoding="utf-8") as file:
        raw_scenarios = json.load(file)
    return [
        Scenario.model_validate(item)
        for item in raw_scenarios
    ]

def main() -> None:
    """Execute all scenarios and print their results."""
    scenarios = load_scenarios()
    for scenario in scenarios:
        result = run_scenario(scenario)
        print(f"\nScenario: {scenario.title}")
        print(f"ID: {result.scenario_id}")
        print(f"Status: {result.status}")
        print(
            f"Steps: {result.passed_steps}/{result.total_steps} passed"
        )
        for step in result.results:
            status = "PASS" if step.passed else "FAIL"
            print(f"  [{status}] {step.description}")

if __name__ == "__main__":
    main()