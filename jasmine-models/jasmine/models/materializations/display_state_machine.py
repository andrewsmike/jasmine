"""
Maintaining materializations' life cycles is a reasonably complex process.
To handle this complexity, and make the celery-job database-state target-db-state
semantics more visible, jasmine explicitly models materializations using state machines and events.
This explicit description makes materialization lifecycles debuggable and easier to deal with.

You can visualize these state machines using the display_materialization_states command.

Some definitions:
- States: The current state of a materialization. Most materializations follow similar state transition patterns.
- Events: A trigger that may change the materialization's state. These are sourced from cron schedules, users,
    external webhooks, or or admin actions.
- Event outcomes: Possible outcome states for each event.
- Event progressive verb: Something that looks nice when written as "{Kill}ing..."
"""
from os.path import basename
from sys import argv

from graphviz import Digraph

from jasmine.models.materializations import materialization_type

state_color = {
    "proposed": "yellow",
    "accepted": "lime",
    "active": "green",
    "could_not_create": "red",
    "bad_spec": "red",
    "terminated": "orange",
}


def upper_first_char(value: str) -> str:
    return value[:1].upper() + value[1:]


def camel_case(value: str) -> str:
    return " ".join(
        upper_first_char(value_part)
        for value_part in value.replace("_", " ").split(" ")
    )


def snake_case(value: str) -> str:
    return value.replace(" ", "_").lower()


def render_state_machine(
    state_machine,
    render_path: str | None = None,
    show: bool = False,
):
    title = state_machine.nice_name + " State Transitions"
    graph = Digraph(name=snake_case(title), comment=title, format="png")

    for state in sorted(state_machine.states):
        graph.node(state, camel_case(state), color=state_color.get(state, "black"))

    for state, events in sorted(state_machine.state_events.items()):
        for event in sorted(events):
            for event_outcome in sorted(state_machine.event_outcomes.get(event, set())):
                graph.edge(state, event_outcome, label=f"{event}")

    graph.render(filename=render_path, cleanup=True, view=show)


event_color = {
    "init": "yellow",
    "verify": "yellow",
    "create": "lime",
    "trim": "green",
    "terminate": "orange",
    "stay_dead": "red",
}


def render_state_machine_event_transitions(
    state_machine,
    render_path: str | None = None,
    show: bool = False,
):
    title = state_machine.nice_name + " Event Transitions"
    graph = Digraph(name=snake_case(title), comment=title, format="png")

    for event in sorted(state_machine.events | {"init", "stay_dead"}):
        graph.node(event, camel_case(event), color=event_color.get(event, "black"))

    for event, outcome_states in sorted(state_machine.event_outcomes.items()):
        for outcome_state in outcome_states:
            for outcome_event in sorted(
                state_machine.state_events.get(outcome_state, {"stay_dead"})
            ):
                graph.edge(event, outcome_event, label=f"{outcome_state}")

    for first_event in state_machine.state_events[state_machine.start_state]:
        graph.edge("init", first_event, label=f"{state_machine.start_state}")

    graph.render(filename=render_path, view=show, cleanup=True)


def display_state_machine():
    if len(argv) != 2:
        print(f"Usage: {basename(argv[0])} {{materialization_name}}")
        print(f"Materializations: {', '.join(materialization_type.keys())}")
        exit(-1)

    materialization_name = argv[1]

    state_machine = materialization_type[materialization_name].state_machine_type

    render_state_machine(
        state_machine,
        show=True,
    )

    render_state_machine_event_transitions(
        state_machine,
        show=True,
    )
