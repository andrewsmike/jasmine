from typing import Any, Literal, Type

from jasmine.models.materializations.base import (
    Event,
    Materialization,
    State,
    StateMachine,
)
from jasmine.models.model_registry import orm_registry

IncrementalState = Literal[
    "proposed",
    "rejected",
    "accepted",
    "could_not_create",
    "could_not_terminate",
    "active",
    "terminated",
]
IncrementalEvent = Literal[
    "verify",
    "create",
    "update",
    "terminate",
]


class IncrementalStateMachine(StateMachine[IncrementalState, IncrementalEvent]):
    """
    Potential mutating actions:
    - Move
    - Change spec

    Other materializations:
    - ALTERs (rename / reorder columns, change indices, etc)
    - Complete data changes
    - Backfills

    So the kill-respawn strategy is gonna have to be the one for now, then.
    We can then move into hot-swapping, then specific operations can get granular.
    """

    nice_name: str = "Incremental"

    # Hack so we can typecheck state values, but still have them available here.
    states: set[IncrementalState] = set(IncrementalState.__args__)  # type: ignore

    state_desc: dict[State, str] = {
        "proposed": "Received request, need to verify.",
        "rejected": "Materialization specification is invalid for some reason; aborted. See logs for details.",
        "accepted": "Materialization verified; need to create.",
        "could_not_create": "Failed to create materialization; aborted. See logs for details.",
        "active": "Successfully created materialization; active.",
        "could_not_terminate": "Failed to clean up materialization; retrying. See logs for details.",
        "terminated": "Materialization terminated by user.",
    }

    start_state: State = "proposed"

    terminal_states: set[State] = {
        "rejected",
        "terminated",
    }

    # Hack so we can typecheck event values, but still have them available here.
    events: set[IncrementalEvent] = set(IncrementalEvent.__args__)  # type: ignore

    state_events: dict[State, set[Event]] = {
        "proposed": {"verify", "terminate"},
        "accepted": {"create", "terminate"},
        "could_not_create": {"terminate"},
        "active": {"update", "terminate"},
        "could_not_terminate": {"terminate"},
    }

    event_progressive_verb: dict[Event, str] = {
        "verify": "verifying",
        "create": "creating",
        "update": "updating",
        "terminate": "terminating",
    }
    event_outcomes: dict[Event, set[State]] = {
        "verify": {"rejected", "accepted"},
        "create": {"could_not_create", "active"},
        "update": {"active"},
        "terminate": {"could_not_terminate", "terminated"},
    }

    state_automatic_event: dict[State, Event] = {
        "proposed": "verify",
        "accepted": "create",
        "could_not_create": "terminate",
        "could_not_terminate": "terminate",  # TODO: Move to slow rescheduled / backoff
    }
    user_events: set[Event] = {
        "terminate",
    }
    scheduled_events: dict[State, set[Event]] = {
        "active": {"update"},
    }


@orm_registry.mapped
class IncrementalMaterialization(Materialization):
    acceptable_view_types = {"query"}
    state_machine_type: Type[StateMachine] = IncrementalStateMachine
    materialization_name: str = "incremental"

    config_types: dict[str, Type[Any]] = {}

    __mapper_args__ = {
        "polymorphic_identity": "incremental",
    }
