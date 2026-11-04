from typing import Literal
from pydantic import BaseModel, Field

ToolName = Literal[
    "check_user_exists",
    "validate_credentials",
    "check_dashboard_access",
]

class ScenarioStep(BaseModel):
    """A single action the QA agent should execute."""
    description: str = Field(min_length=1)
    tool: ToolName
    parameters: dict[str, str] = Field(default_factory=dict)
    expected_result: bool

class Scenario(BaseModel):
    """Input scenario provided to the QA agent."""
    scenario_id: str
    title: str
    steps: list[ScenarioStep] = Field(min_length=1)

class StepResult(BaseModel):
    """Result of executing one test step."""
    description: str
    tool: ToolName
    actual_result: bool
    expected_result: bool
    passed: bool

class AgentRunResult(BaseModel):
    """Structured summary of the complete agent execution."""
    scenario_id: str
    status: Literal["passed", "failed"]
    total_steps: int
    passed_steps: int
    failed_steps: int
    results: list[StepResult]