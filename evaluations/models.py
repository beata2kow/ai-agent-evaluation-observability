
from typing import Literal
from pydantic import BaseModel, Field

class ScenarioEvaluation(BaseModel):
    """Evaluation result for a single agent scenario."""

    scenario_id: str
    expected_status: Literal["passed", "failed"]
    actual_status: Literal["passed", "failed"]
    status_matches: bool
    task_completed: bool
    total_steps: int = Field(ge=1)
    correct_steps: int = Field(ge=0)
    step_accuracy: float = Field(ge=0.0, le=1.0)

class EvaluationReport(BaseModel):
    """Aggregated evaluation metrics for the complete dataset."""

    dataset_name: str
    dataset_version: str
    total_scenarios: int = Field(ge=1)
    completed_scenarios: int = Field(ge=0)
    task_completion_rate: float = Field(ge=0.0, le=1.0)
    total_steps: int = Field(ge=1)
    correct_steps: int = Field(ge=0)
    step_accuracy: float = Field(ge=0.0, le=1.0)
    scenario_results: list[ScenarioEvaluation] = Field(min_length=1)
