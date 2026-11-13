
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4
from observability.models import AgentTrace, TraceEvent

class TraceRecorder:
    """Record structured events during a single agent execution."""
    def __init__(self, scenario_id: str):
        self._trace = AgentTrace(
            run_id=str(uuid4()),
            scenario_id=scenario_id,
            started_at=self._now(),
        )
        self._add_event(
            event_type="scenario.started",
        )

    @staticmethod
    def _now() -> datetime:
        """Return the current UTC timestamp."""
        return datetime.now(timezone.utc)

    def _add_event(
        self,
        event_type: str,
        step_number: int | None = None,
        tool_name: str | None = None,
        duration_ms: float | None = None,
        status: str | None = None,
        error_type: str | None = None,
        error_message: str | None = None,
    ) -> None:
        """Create and append an event to the current trace."""
        event = TraceEvent(
            event_id=str(uuid4()),
            run_id=self._trace.run_id,
            scenario_id=self._trace.scenario_id,
            event_type=event_type,
            timestamp=self._now(),
            step_number=step_number,
            tool_name=tool_name,
            duration_ms=duration_ms,
            status=status,
            error_type=error_type,
            error_message=error_message,
        )
        self._trace.events.append(event)

    def record_tool_started(
        self,
        step_number: int,
        tool_name: str,
    ) -> float:
        """Record tool execution start and return a monotonic timer value."""
        self._add_event(
            event_type="tool.started",
            step_number=step_number,
            tool_name=tool_name,
        )
        return perf_counter()

    def record_tool_completed(
        self,
        step_number: int,
        tool_name: str,
        started_counter: float,
    ) -> None:
        """Record successful tool execution and its duration."""
        duration_ms = (perf_counter() - started_counter) * 1000
        self._add_event(
            event_type="tool.completed",
            step_number=step_number,
            tool_name=tool_name,
            duration_ms=duration_ms,
            status="success",
        )

    def record_tool_failed(
        self,
        step_number: int,
        tool_name: str,
        started_counter: float,
        error: Exception,
    ) -> None:
        """Record failed tool execution, duration and error details."""
        duration_ms = (perf_counter() - started_counter) * 1000
        self._add_event(
            event_type="tool.failed",
            step_number=step_number,
            tool_name=tool_name,
            duration_ms=duration_ms,
            status="failure",
            error_type=type(error).__name__,
            error_message=str(error),
        )

    def record_scenario_completed(self) -> None:
        """Record the completion of the scenario."""
        self._add_event(
            event_type="scenario.completed",
        )
        self._trace.completed_at = self._trace.events[-1].timestamp

    def get_trace(self) -> AgentTrace:
        """Return the complete execution trace."""
        return self._trace
