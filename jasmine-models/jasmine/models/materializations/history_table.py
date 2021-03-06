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

HistoryTableState = Literal[
    "proposed",
    "bad_spec",
    "accepted",
    "could_not_create",
    "active",
    "could_not_terminate",
    "terminated",
]
HistoryTableEvent = Literal[
    "verify",
    "create",
    "trim",
    "terminate",
]


class HistoryTableStateMachine(StateMachine[HistoryTableState, HistoryTableEvent]):
    """
    How do you purge from history? DELETE the materialization logs and row? Rely on sqlalchemy?
    Note: You can't pause / unpause history tables without losing data. Don't offer it as an option here.
    What about various migration cases? How do you manipulate the underlying table without flushing?
    Is there a valid reason to pause a history materialization (IE, remove the triggers?)
    Should we give users a mechanism they can use to recreate the triggers later?

    How about suspend / resume triggers? Or verifying triggers / schema still match every run?
    """

    nice_name: str = "History Table"

    # Hack so we can typecheck state values, but still have them available here.
    states: set[HistoryTableState] = set(HistoryTableState.__args__)  # type: ignore

    state_desc: dict[State, str] = {
        "proposed": "Received request, need to verify.",
        "bad_spec": "Materialization specification is invalid for some reason; aborted. See logs for details.",
        "accepted": "Materialization verified; need to create.",
        "could_not_create": "Failed to create materialization; aborted. See logs for details.",
        "active": "Successfully created materialization; active.",
        "could_not_terminate": "Failed to clean up materialization; retrying. See logs for details.",
        "terminated": "Materialization terminated by user.",
    }

    start_state: State = "proposed"

    terminal_states: set[State] = {
        "bad_spec",
        "terminated",
    }

    # Hack so we can typecheck event values, but still have them available here.
    events: set[HistoryTableEvent] = set(HistoryTableEvent.__args__)  # type: ignore

    state_events: dict[State, set[Event]] = {
        "proposed": {"verify", "terminate"},
        "accepted": {"create", "terminate"},
        "active": {"trim", "terminate"},
        "could_not_create": {"terminate"},
        "could_not_terminate": {"terminate"},
    }

    event_progressive_verb: dict[Event, str] = {
        "verify": "verifying",
        "create": "creating",
        "trim": "trimming",
        "terminate": "terminating",
    }
    event_outcomes: dict[Event, set[State]] = {
        "verify": {"bad_spec", "accepted"},
        "create": {"could_not_create", "active"},
        "trim": {"active"},  # TODO: Add migration-friendly failure/restart options.
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
class HistoryTableMaterialization(Materialization):
    state_machine_type: Type[StateMachine] = HistoryTableStateMachine
    materialization_name: str = "history_table"
    acceptable_view_types = {"history_table"}

    config_types: dict[str, Type[Any]] = {
        "source_database": str,
        "source_table": str,
        "retention_period_seconds": int,
        "trim_frequency_seconds": int,
    }

    __mapper_args__ = {
        "polymorphic_identity": "history_table",
    }

    @property
    def table_name(self) -> str:
        return self.view.spec["source_table_name"] + "_history"
