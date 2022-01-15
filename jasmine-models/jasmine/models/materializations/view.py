from typing import Any, Literal, Type

from jasmine.models.materializations.base import (
    Event,
    Materialization,
    State,
    StateMachine,
)
from jasmine.models.model_registry import orm_registry

ViewState = Literal[
    "proposed",
    "rejected",
    "accepted",
    "could_not_create",
    "could_not_terminate",
    "active",
    "terminated",
]
ViewEvent = Literal[
    "verify",
    "create",
    "terminate",
]


class ViewStateMachine(StateMachine[ViewState, ViewEvent]):
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

    nice_name: str = "Database View"

    # Hack so we can typecheck state values, but still have them available here.
    states: set[ViewState] = set(ViewState.__args__)  # type: ignore

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
    events: set[ViewEvent] = set(ViewEvent.__args__)  # type: ignore

    state_events: dict[State, set[Event]] = {
        "proposed": {"verify", "terminate"},
        "accepted": {"create", "terminate"},
        "could_not_create": {"terminate"},
        "active": {"terminate"},
        "could_not_terminate": {"terminate"},
    }

    event_progressive_verb: dict[Event, str] = {
        "verify": "verifying",
        "create": "creating",
        "terminate": "terminating",
    }
    event_outcomes: dict[Event, set[State]] = {
        "verify": {"rejected", "accepted"},
        "create": {"could_not_create", "active"},
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
    scheduled_events: set[Event] = set()


@orm_registry.mapped
class ViewMaterialization(Materialization):
    acceptable_view_types = {"query"}
    state_machine_type: Type[StateMachine] = ViewStateMachine
    materialization_name: str = "view"

    config_types: dict[str, Type[Any]] = {}

    __mapper_args__ = {
        "polymorphic_identity": "view",
    }
