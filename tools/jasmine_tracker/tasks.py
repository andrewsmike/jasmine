from dataclasses import dataclass
from functools import partial
from itertools import zip_longest
from pprint import pformat
from typing import Any, Optional

__all__ = [
    "Task",
]


def parse_task_set(task_list_str: Optional[str]) -> frozenset[int]:
    result = []
    for task in (task_list_str or "").split():
        task = task.strip(",")
        if not task:
            continue
        task_id = int(task.split("-")[1])
        result.append(task_id)

    return frozenset(result)


def parse_int(value: str) -> int:
    return int(value) if value else 0


def parse_opt_int(value: str) -> Optional[int]:
    if value:
        return int(value)
    else:
        return None


def parse_opt_float(value: str) -> Optional[float]:
    return float(value) if value else None


def parse_enum(values: list[Any], value: Any) -> Any:
    assert value in values, f"Value {value} not in {values}!"
    return value


def value_str(value: Any) -> str:
    if isinstance(value, frozenset):
        return ", ".join(f"task-{subtask}" for subtask in sorted(value))
    else:
        return str(value)


@dataclass(eq=True, frozen=True)
class Task:
    task_id: int
    task_type: str
    role: Optional[str]
    desc: str
    status: str
    value: int
    effort: int
    depends_on: frozenset[int]
    best_value: int
    best_effort: int
    priority: float
    best_followups: frozenset[int]

    statuses = [
        f"{i+1} - {status}"
        for i, status in enumerate(["TODO", "WIP", "BLOCKED", "DONE", "NOPE", "IDEA"])
    ]

    ordered_column_parsing_funcs = [
        ("task_id", int),
        ("task_type", partial(parse_enum, ["Story", "Task"])),
        ("role", str),
        ("desc", str),
        ("status", partial(parse_enum, statuses)),
        ("value", parse_int),
        ("effort", parse_int),
        ("depends_on", parse_task_set),
        ("best_value", parse_opt_int),
        ("best_effort", parse_opt_int),
        ("priority", parse_opt_float),
        ("best_followups", parse_task_set),
    ]

    @classmethod
    def from_row(cls, row: list[Any]) -> "Task":
        try:
            return cls(
                **{
                    key: parse_value_func(value)
                    for (value, (key, parse_value_func)) in zip_longest(
                        row,
                        Task.ordered_column_parsing_funcs,
                    )
                }
            )
        except AssertionError as e:
            task = {
                key: value
                for (value, (key, _)) in zip_longest(
                    row,
                    Task.ordered_column_parsing_funcs,
                )
            }
            raise ValueError(f"Could not parse task {pformat(task)}:\n{e}")

    def row(self) -> list[Any]:
        return [
            value_str(getattr(self, key))
            for (key, _) in Task.ordered_column_parsing_funcs
        ]
