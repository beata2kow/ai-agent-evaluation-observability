
import json
from pathlib import Path

from agent.main import run_scenario
from agent.models import Scenario, GoldenDataset
from evaluations.evaluator import evaluate_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCENARIOS_PATH = PROJECT_ROOT / "datasets" / "login_scenarios.json"
GOLDEN_DATASET_PATH = PROJECT_ROOT / "evaluations" / "golden_dataset.json"
REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_report.json"


def load_scenarios() -> list[Scenario]:
    """Load and validate execution scenarios from JSON."""
    with SCENARIOS_PATH.open(encoding="utf-8") as file:
        raw_scenarios = json.load(file)

    return [
        Scenario.model_validate(item)
        for item in raw_scenarios
    ]


def load_golden_dataset() -> GoldenDataset:
    """Load and validate the golden evaluation dataset."""
    with GOLDEN_DATASET_PATH.open(encoding="utf-8") as file:
        raw_dataset = json.load(file)

    return GoldenDataset.model_validate(raw_dataset)


def main() -> None:
    """Execute scenarios, evaluate results and generate a report."""

    # 1. Load execution scenarios.
    scenarios = load_scenarios()

    # 2. Execute the agent against every scenario.
    agent_results = []

    for scenario in scenarios:
        result = run_scenario(scenario)
        agent_results.append(result)

        print(f"\nScenario: {scenario.title}")
        print(f"ID: {result.scenario_id}")
        print(f"Status: {result.status}")
        print(
            f"Steps: {result.passed_steps}/{result.total_steps} passed"
        )

        for step in result.results:
            status = "PASS" if step.passed else "FAIL"
            print(f"  [{status}] {step.description}")

    # 3. Load the independent golden dataset.
    golden_dataset = load_golden_dataset()

    # 4. Evaluate actual agent results.
    report = evaluate_dataset(
        agent_results=agent_results,
        golden_dataset=golden_dataset,
    )

    # 5. Print the evaluation summary.
    print("\n" + "=" * 50)
    print("AGENT EVALUATION REPORT")
    print("=" * 50)

    print(f"Dataset: {report.dataset_name}")
    print(f"Version: {report.dataset_version}")
    print(f"Total scenarios: {report.total_scenarios}")
    print(
        f"Completed scenarios: "
        f"{report.completed_scenarios}/{report.total_scenarios}"
    )
    print(
        f"Task completion rate: "
        f"{report.task_completion_rate:.2%}"
    )
    print(f"Total steps: {report.total_steps}")
    print(f"Correct steps: {report.correct_steps}")
    print(f"Step accuracy: {report.step_accuracy:.2%}")

    print("\nScenario evaluation details:")

    for result in report.scenario_results:
        print(f"\n  Scenario: {result.scenario_id}")
        print(f"  Task completed: {result.task_completed}")
        print(f"  Status matches: {result.status_matches}")
        print(
            f"  Step accuracy: {result.correct_steps}/"
            f"{result.total_steps} ({result.step_accuracy:.2%})"
        )

    # 6. Save the evaluation report as JSON.
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        report.model_dump_json(indent=2),
        encoding="utf-8",
    )

    print(f"\nEvaluation report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
