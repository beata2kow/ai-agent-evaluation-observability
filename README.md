# AI Agent Evaluation & Observability Framework

An independent portfolio project focused on evaluating, testing, and
monitoring AI agents.

## Project goals

- Build a reproducible evaluation dataset.
- Measure agent correctness and task completion.
- Evaluate tool selection and tool usage.
- Track agent execution and errors.
- Detect regressions through automated evaluations.
- Explore continuous evaluation in CI/CD pipelines.

## Project structure

- `agent/` – agent implementation and prompts.
- `datasets/` – evaluation and adversarial test cases.
- `evaluations/` – evaluation metrics and evaluators.
- `observability/` – tracing and monitoring.
- `tests/` – automated tests.
- `reports/` – generated evaluation reports.

## Development setup

- Python 3.12 is recommended.
- python3.12 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- pytest


## Status 
Work in progress. This project is developed independently
using synthetic test scenarios and publicly shareable examples.
