from typing import Any, Literal, Type

from jasmine.models.materializations.base import (
    Event,
    Materialization,
    State,
    StateMachine,
)
from jasmine.models.model_registry import orm_registry

SECONDS = 1
MINUTES = 60 * SECONDS
HOURS = 60 * MINUTES
DAYS = 24 * HOURS

ViewState = Literal[
    "proposed",
    "rejected",
    "accepted",
    "could_not_create",
    "active",
    "terminated",
]
ViewEvent = Literal[
    "verify",
    "create",
    "terminate",
]


class ViewStateMachine(StateMachine[ViewState, ViewEvent]):
    """ """

    nice_name: str = "Database View"

    # Hack so we can typecheck state values, but still have them available here.
    states: set[ViewState] = set(ViewState.__args__)

    state_desc: dict[State, str] = {
        "proposed": "Received request, need to verify.",
        "rejected": "Materialization specification is invalid for some reason; aborted. See logs for details.",
        "accepted": "Materialization verified; need to create.",
        "could_not_create": "Failed to create materialization; aborted. See logs for details.",
        "active": "Successfully created materialization; active.",
        "terminated": "Materialization terminated by user.",
    }

    start_state: State = "proposed"

    terminal_states: set[State] = {
        "rejected",
        "could_not_create",
        "terminated",
    }

    # Hack so we can typecheck event values, but still have them available here.
    events: set[ViewEvent] = set(ViewEvent.__args__)

    state_events: dict[State, set[Event]] = {
        "proposed": {"verify", "terminate"},
        "accepted": {"create", "terminate"},
        "active": {"terminate"},
    }

    event_progressive_verb: dict[Event, str] = {
        "verify": "verifying",
        "create": "creating",
        "terminate": "terminating",
    }
    event_outcomes: dict[Event, set[State]] = {
        "verify": {"rejected", "accepted"},
        "create": {"could_not_create", "active"},
        "terminate": {"terminated"},
    }

    automatic_events: set[Event] = {"verify", "create"}
    user_events: set[Event] = {
        "terminate",
    }
    scheduled_events: set[Event] = {}


@orm_registry.mapped
class ViewMaterialization(Materialization):
    acceptable_view_types = {"query"}
    state_machine_type: Type[StateMachine] = ViewStateMachine
    materialization_name: str = "view"

    config_types: dict[str, Type[Any]] = {}
    config_defaults: dict[str, Any | None] = {}

    __mapper_args__ = {
        "polymorphic_identity": "view",
    }
