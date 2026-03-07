from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from .workspace import (
    Workspace,
    blocked_tasks,
    due_soon_tasks,
    overdue_actions,
    overdue_tasks,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="work-codex")
    parser.add_argument("--workspace", default=".", help="Path to the workspace root")

    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "status", "followup"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--workspace", default=".", help=argparse.SUPPRESS)
    return parser


def _print_task_group(title: str, tasks: list) -> None:
    print(title)
    if not tasks:
        print("  none")
        return
    for task in tasks:
        due = task.due.isoformat() if task.due else "none"
        print(f"  [{task.priority}] #{task.id} {task.title} ({task.company}, due {due})")


def _print_action_group(title: str, actions: list) -> None:
    print(title)
    if not actions:
        print("  none")
        return
    for action in actions:
        due = action.next_action_date.isoformat() if action.next_action_date else "none"
        print(f"  [{action.source}] {action.name} ({action.company}, due {due})")
        print(f"    {action.next_action}")


def run(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    workspace = Workspace(Path(args.workspace).resolve())
    today = date.today()

    if args.command == "validate":
        errors = workspace.validate()
        if errors:
            print("validation failed")
            for error in errors:
                print(f"- {error}")
            return 1
        print("validation passed")
        print(f"memory records: {workspace.memory_record_count()}")
        return 0

    validation_errors = workspace.validate()
    if validation_errors:
        print("workspace is not ready")
        for error in validation_errors:
            print(f"- {error}")
        return 1

    tasks = workspace.tasks()
    pipeline = workspace.pipeline_actions()
    funding = workspace.funding_actions()

    if args.command == "status":
        print(f"status for {workspace.root}")
        _print_task_group("overdue tasks", overdue_tasks(tasks, today))
        _print_task_group("due soon tasks", due_soon_tasks(tasks, today))
        _print_task_group("blocked tasks", blocked_tasks(tasks))
        print("at-risk goals")
        risks = workspace.goal_risks()
        if not risks:
            print("  none")
        else:
            for risk in risks:
                print(f"  [{risk.owner}] {risk.objective}")
                print(f"    {risk.description}")
                print(f"    current: {risk.current}")
        _print_action_group(
            "overdue pipeline next actions", overdue_actions(pipeline, today)
        )
        _print_action_group(
            "overdue funding next actions", overdue_actions(funding, today)
        )
        return 0

    if args.command == "followup":
        followups = overdue_tasks(tasks, today)
        followups.extend(blocked_tasks(tasks))
        print("follow-up queue")
        if not followups and not overdue_actions(pipeline, today) and not overdue_actions(
            funding, today
        ):
            print("  none")
            return 0
        for task in followups:
            due = task.due.isoformat() if task.due else "none"
            print(f"  task #{task.id}: {task.title} ({task.status}, due {due})")
        for action in overdue_actions(pipeline, today):
            due = action.next_action_date.isoformat() if action.next_action_date else "none"
            print(f"  pipeline: {action.name} (due {due})")
        for action in overdue_actions(funding, today):
            due = action.next_action_date.isoformat() if action.next_action_date else "none"
            print(f"  funding: {action.name} (due {due})")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(run())
