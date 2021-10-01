from dataclasses import replace
from functools import cache
from itertools import chain, combinations
from typing import Dict, Tuple

from jasmine_tracker import gsheet_jasmine_tasks, update_gsheet_jasmine_tasks
from tasks import Task


@cache
def task_by_id(tasks: frozenset[Task]) -> Dict[int, Task]:
    return {task.task_id: task for task in tasks}


@cache
def task_ancestors(task: Task, tasks: frozenset[Task]) -> set[Task]:
    task_id_task = task_by_id(tasks)

    current_tasks: set[Task] = set()
    new_tasks = {task}
    while new_tasks:
        current_tasks |= new_tasks
        new_tasks = {
            task_id_task[ancestor_task_id]
            for task in new_tasks
            for ancestor_task_id in task.depends_on
        } - current_tasks

    return current_tasks - {task}


def task_descendents(parent_task: Task, tasks: set[Task]) -> set[Task]:
    task_ancestor_tasks = {
        task: task_ancestors(task, frozenset(tasks)) for task in tasks
    }

    return {task for task in tasks if parent_task in task_ancestor_tasks[task]}


def taskset_value_effort(tasks: set[Task]) -> Tuple[int, int]:
    return (
        sum(task.value for task in tasks),
        sum(task.effort for task in tasks),
    )


def tasks_required_value_effort(
    tasks: set[Task], all_tasks: set[Task]
) -> Tuple[int, int]:
    required_tasks = {
        required_task
        for task in tasks
        for required_task in (task_ancestors(task, frozenset(all_tasks)) | {task})
        if "DONE" not in required_task.status
    }

    return taskset_value_effort(required_tasks)


def subsets(values):
    return chain.from_iterable(combinations(values, r) for r in range(len(values) + 1))


def taskset_priority(tasks: set[Task], all_tasks: set[Task]) -> float:
    value, effort = tasks_required_value_effort(tasks, all_tasks)
    return (value + 0.5) / (effort + 0.5)


def best_taskset(
    possible_tasks: set[Task],
    required_tasks: set[Task],
    all_tasks: set[Task],
) -> set[Task]:
    return max(
        (
            (set(task_set) | required_tasks)
            for task_set in subsets(possible_tasks - required_tasks)
        ),
        key=lambda taskset: (taskset_priority(taskset, all_tasks), -len(taskset)),
    )


def task_with_best_priority(task: Task, tasks: set[Task]) -> Task:
    best_descendent_taskset = best_taskset(
        task_descendents(task, tasks),
        required_tasks={task},
        all_tasks=tasks,
    )

    best_value, best_effort = tasks_required_value_effort(
        best_descendent_taskset,
        tasks,
    )

    best_followups = {
        followup_task.task_id for followup_task in (best_descendent_taskset - {task})
    }

    blocked_by = {
        blocking_ancestor.task_id
        for blocking_ancestor in task_ancestors(task, frozenset(tasks))
        if "DONE" not in blocking_ancestor.status
    }

    return replace(
        task,
        best_value=best_value,
        best_effort=best_effort,
        priority=(best_value + 0.5) / (best_effort + 0.5),
        best_followups=best_followups,
        blocked_by=blocked_by,
    )


def update_backlog():
    tasks = set(gsheet_jasmine_tasks())
    tasks = [
        task_with_best_priority(task, tasks)
        for task in sorted(tasks, key=lambda task: task.task_id)
    ]
    update_gsheet_jasmine_tasks(tasks)


if __name__ == "__main__":
    update_backlog()
