"""
Code interactions:
- Frontend:
    - Create new materialization with given config, view. [DONE]
    - Trigger events (terminate, etc) [DONE]
    - Query status of materialization. [one_event]
    - Interrupt current event, cancel triggered events within time window [one_event]
    - View BackendEvents associated with materialization. [logs]

- TODO: Proper current_event(), mutex locking, interruptions [one_event]
- TODO: Multiple sessions for proper exception handling, figure out way to integrate debug messages. [logs]

- Backend:
    - Run triggered events against DB [DONE]
    - Transition to a different state [DONE]
    - Return results (schema queries, status/monitoring queries, etc) [redis_celery_cache]
    - Ensure all events are atomic and can be killed, reran safely [safe_rollback]

- TODO: Set up redis-caching-over-celery pattern. [redis_celery_cache]
- TODO: ... Atomic DDL is kinda hard. Work on this a bit. [safe_rollback]

- "System":
    - Cache returned results [DONE]
    - Cache and refresh materialization property / status queries [DONE]
    - Allow users to inject new events [DONE]
    - Trigger next automatic events [auto_trigger]
    - Rerun failed events [auto_trigger]
    - Configure next scheduled events [schedule_trigger]
    - Ensure only one event runs at a time [one_event]
    - Ensure currently running events can be killed (or waited out) [one_event]
    - Handle backoff mechanisms [trigger_errors]
    - Trigger failed-to-run transitions [trigger_errors]
    - Retrigger automatic events, handle stale user requests, and reconfigure schedule when restarting backend [auto_trigger]

- TODO: Autotrigger automatic transitions, event across celery restarts and other errors. [auto_trigger]
- TODO: Correctly trigger scheduled transitions, nicely handling celery restarts, failed tasks, and other errors. [schedule_trigger]
- TODO: Handle failed tasks in a principled and sane way, such as with retries, backoffs, and default failure states. [trigger_errors]


- Failure cases: Failure...
    - To launch the next event [trigger_errors]
    - To update schedule [safe_rollback]
    - To update the DB [safe_rollback]
    - To run the task (at all) after it has been launched [safe_rollback]
    - That want to retry immediately [trigger_errors]
    - That want to retry over a large timeframe [trigger_errors]
    - Etc

- I need to cache temporary references to celery tasks (for aborting, result waiting / fetching, UNDO operation, etc)
"""
from typing import Generic, Type, TypeVar

from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    Enum,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from jasmine.models.model_registry import orm_registry

materialization_types = [
    "view",
    "history_table",
]

# Each subclass needs to define their own State / Event types.
# To handle this, have the parent class be generic against these.
State = TypeVar("State")
Event = TypeVar("Event")


class StateMachine(Generic[State, Event]):
    nice_name: str

    states: set[State]
    state_desc: dict[State, str]

    start_state: State
    terminal_states: set[State]

    events: set[Event]
    state_events: dict[State, set[Event]]
    event_progressive_verb: dict[Event, str]
    event_outcomes: dict[Event, set[State]]

    state_automatic_event: dict[State, Event]
    user_events: dict[State, set[Event]]
    scheduled_events: dict[State, set[Event]]


@orm_registry.mapped
class Materialization:
    materialization_name: str
    state_machine_type: Type[StateMachine]
    acceptable_view_types: set[str]

    __tablename__ = "materializations"
    materialization_id = Column(BigInteger, nullable=False)

    materialization_type = Column(Enum(*materialization_types), nullable=False)

    state = Column(String(64), nullable=False)

    # Static configuration determined on creation.
    config = Column(MutableDict.as_mutable(JSON), nullable=False)
    context = Column(MutableDict.as_mutable(JSON), nullable=False)

    view_id = Column(BigInteger, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("materialization_id"),
        UniqueConstraint("view_id", "materialization_type"),
        ForeignKeyConstraint(["view_id"], ["views.view_id"]),
    )

    view = relationship("View", backref="materializations")

    __mapper_args__ = {
        # Note: You can't instantiate base materializations.
        # The type enum won't allow it, and it doesn't make sense.
        "polymorphic_identity": "none",
        "polymorphic_on": materialization_type,
    }

    @property
    def db_name(self) -> str:
        return self.view.project.backend.spec["connection_args"]["database"]

    @property
    def table_name(self) -> str:
        return f"{self.view.path}_{self.materialization_name}"

    def update_context(self):
        self.context = dict(self.context)
