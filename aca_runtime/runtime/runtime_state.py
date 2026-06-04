from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RuntimeEvent:
    event_type: str
    text: str
    state: str
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AcceptedTurn:
    text: str
    measurements: Dict[str, Any] = field(default_factory=dict)
    triaxial_profile: Optional[Dict[str, Any]] = None
    diagnostics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RejectedTurn:
    text: str
    state: str
    reason: str
    measurements: Dict[str, Any] = field(default_factory=dict)
    diagnostics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeState:
    """
    ACA Runtime v2 semantic state.

    Core invariant:
    A non-admitted input must never alter the accepted origin
    or accepted trajectory.
    """

    origin: Optional[AcceptedTurn] = None
    objective: Optional[str] = None
    accepted_trajectory: List[AcceptedTurn] = field(default_factory=list)
    rejected_inputs: List[RejectedTurn] = field(default_factory=list)
    runtime_events: List[RuntimeEvent] = field(default_factory=list)

    def has_origin(self) -> bool:
        return self.origin is not None

    def trajectory_length(self) -> int:
        return len(self.accepted_trajectory)

    def rejected_count(self) -> int:
        return len(self.rejected_inputs)

    def accept_origin(
        self,
        text: str,
        measurements: Dict[str, Any],
        triaxial_profile: Optional[Dict[str, Any]] = None,
        diagnostics: Optional[Dict[str, Any]] = None,
        objective: Optional[str] = None,
    ) -> None:
        """
        Creates a new semantic origin.

        This resets the accepted trajectory because a new origin defines
        a new accepted semantic path.
        """

        turn = AcceptedTurn(
            text=text,
            measurements=measurements,
            triaxial_profile=triaxial_profile,
            diagnostics=diagnostics or {},
        )

        self.origin = turn
        self.objective = objective
        self.accepted_trajectory = [turn]

        self.runtime_events.append(
            RuntimeEvent(
                event_type="origin_created",
                text=text,
                state="ACCEPT_AS_ORIGIN",
                reason="Input accepted as semantic origin.",
                metadata={
                    "objective": objective,
                    "trajectory_length": self.trajectory_length(),
                },
            )
        )

    def accept_continuation(
        self,
        text: str,
        measurements: Dict[str, Any],
        triaxial_profile: Optional[Dict[str, Any]] = None,
        diagnostics: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Appends a valid continuation to the accepted trajectory.

        A continuation requires an existing origin.
        """

        if not self.has_origin():
            raise RuntimeError(
                "Cannot accept continuation before semantic origin exists."
            )

        turn = AcceptedTurn(
            text=text,
            measurements=measurements,
            triaxial_profile=triaxial_profile,
            diagnostics=diagnostics or {},
        )

        self.accepted_trajectory.append(turn)

        self.runtime_events.append(
            RuntimeEvent(
                event_type="trajectory_updated",
                text=text,
                state="ACCEPT_AS_CONTINUATION",
                reason="Input accepted as trajectory continuation.",
                metadata={
                    "trajectory_length": self.trajectory_length(),
                },
            )
        )

    def reject_input(
        self,
        text: str,
        state: str,
        reason: str,
        measurements: Dict[str, Any],
        diagnostics: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Stores a rejected, unclear, restricted, or out-of-field input.

        This method must never modify:
        - origin
        - objective
        - accepted_trajectory
        """

        before_origin = self.origin
        before_objective = self.objective
        before_trajectory_length = self.trajectory_length()

        self.rejected_inputs.append(
            RejectedTurn(
                text=text,
                state=state,
                reason=reason,
                measurements=measurements,
                diagnostics=diagnostics or {},
            )
        )

        self.runtime_events.append(
            RuntimeEvent(
                event_type="input_rejected",
                text=text,
                state=state,
                reason=reason,
                metadata={
                    "accepted_trajectory_length": before_trajectory_length,
                    "rejected_inputs_length": self.rejected_count(),
                },
            )
        )

        assert self.origin is before_origin
        assert self.objective == before_objective
        assert self.trajectory_length() == before_trajectory_length

    def last_accepted_turn(self) -> Optional[AcceptedTurn]:
        if not self.accepted_trajectory:
            return None

        return self.accepted_trajectory[-1]

    def last_rejected_turn(self) -> Optional[RejectedTurn]:
        if not self.rejected_inputs:
            return None

        return self.rejected_inputs[-1]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "has_origin": self.has_origin(),
            "origin_text": self.origin.text if self.origin else None,
            "objective": self.objective,
            "accepted_trajectory_length": self.trajectory_length(),
            "rejected_inputs_length": self.rejected_count(),
            "last_accepted_text": (
                self.last_accepted_turn().text
                if self.last_accepted_turn()
                else None
            ),
            "last_rejected_text": (
                self.last_rejected_turn().text
                if self.last_rejected_turn()
                else None
            ),
            "last_event": (
                asdict(self.runtime_events[-1])
                if self.runtime_events
                else None
            ),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "origin": asdict(self.origin) if self.origin else None,
            "objective": self.objective,
            "accepted_trajectory": [
                asdict(turn)
                for turn in self.accepted_trajectory
            ],
            "rejected_inputs": [
                asdict(turn)
                for turn in self.rejected_inputs
            ],
            "runtime_events": [
                asdict(event)
                for event in self.runtime_events
            ],
            "snapshot": self.snapshot(),
        }