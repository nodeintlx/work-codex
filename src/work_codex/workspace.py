from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import json
from pathlib import Path
from typing import Any

import yaml


REQUIRED_FILES = (
    "shared/tasks.yaml",
    "shared/goals.yaml",
    "shared/pipeline.yaml",
    "shared/funding.yaml",
)


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    company: str
    priority: str
    status: str
    due: date | None
    notes: str

    @property
    def is_open(self) -> bool:
        return self.status != "done"


@dataclass(frozen=True)
class GoalRisk:
    owner: str
    objective: str
    description: str
    status: str
    current: str


@dataclass(frozen=True)
class NextAction:
    source: str
    name: str
    company: str
    next_action: str
    next_action_date: date | None
    risk: str


def _parse_date(value: Any) -> date | None:
    if value in (None, "", "none"):
        return None
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not load as a mapping")
    return data


class Workspace:
    def __init__(self, root: Path):
        self.root = root

    def validate(self) -> list[str]:
        errors: list[str] = []
        for relative_path in REQUIRED_FILES:
            path = self.root / relative_path
            if not path.exists():
                errors.append(f"missing required file: {relative_path}")
        if errors:
            return errors

        try:
            tasks = self.tasks()
            if not tasks:
                errors.append("shared/tasks.yaml contains no tasks")
        except Exception as exc:
            errors.append(f"failed to load tasks: {exc}")

        try:
            _ = self.goal_risks()
        except Exception as exc:
            errors.append(f"failed to load goals: {exc}")

        try:
            _ = self.pipeline_actions()
        except Exception as exc:
            errors.append(f"failed to load pipeline: {exc}")

        try:
            _ = self.funding_actions()
        except Exception as exc:
            errors.append(f"failed to load funding: {exc}")

        return errors

    def tasks(self) -> list[Task]:
        data = _load_yaml(self.root / "shared/tasks.yaml")
        raw_tasks = data.get("tasks", [])
        tasks: list[Task] = []
        for item in raw_tasks:
            tasks.append(
                Task(
                    id=int(item["id"]),
                    title=str(item["title"]),
                    company=str(item["company"]),
                    priority=str(item["priority"]),
                    status=str(item["status"]),
                    due=_parse_date(item.get("due")),
                    notes=str(item.get("notes", "")),
                )
            )
        return tasks

    def goal_risks(self) -> list[GoalRisk]:
        data = _load_yaml(self.root / "shared/goals.yaml")
        risks: list[GoalRisk] = []
        for owner, owner_goals in data.items():
            if owner in {"quarter", "last_updated"}:
                continue
            if not isinstance(owner_goals, dict):
                continue
            for objective in owner_goals.values():
                if not isinstance(objective, dict):
                    continue
                title = str(objective.get("title", owner))
                for key_result in objective.get("key_results", []):
                    status = str(key_result.get("status", ""))
                    if status == "at_risk":
                        risks.append(
                            GoalRisk(
                                owner=owner,
                                objective=title,
                                description=str(key_result.get("description", "")),
                                status=status,
                                current=str(key_result.get("current", "")),
                            )
                        )
        return risks

    def pipeline_actions(self) -> list[NextAction]:
        data = _load_yaml(self.root / "shared/pipeline.yaml")
        return self._next_actions_from_items("pipeline", data.get("deals", []))

    def funding_actions(self) -> list[NextAction]:
        data = _load_yaml(self.root / "shared/funding.yaml")
        return self._next_actions_from_items("funding", data.get("programs", []))

    def _next_actions_from_items(
        self, source: str, items: list[dict[str, Any]]
    ) -> list[NextAction]:
        actions: list[NextAction] = []
        for item in items:
            actions.append(
                NextAction(
                    source=source,
                    name=str(item.get("name", "")),
                    company=str(item.get("company", "")),
                    next_action=str(item.get("next_action", "")),
                    next_action_date=_parse_date(item.get("next_action_date")),
                    risk=str(item.get("risk", "")),
                )
            )
        return actions

    def memory_record_count(self) -> int:
        path = self.root / "knowledge/memory.jsonl"
        if not path.exists():
            return 0
        count = 0
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                json.loads(line)
                count += 1
        return count


def overdue_tasks(tasks: list[Task], today: date) -> list[Task]:
    return [task for task in tasks if task.is_open and task.due and task.due < today]


def due_soon_tasks(tasks: list[Task], today: date, window_days: int = 3) -> list[Task]:
    upper_bound = today + timedelta(days=window_days)
    return [
        task
        for task in tasks
        if task.is_open and task.due and today <= task.due <= upper_bound
    ]


def blocked_tasks(tasks: list[Task]) -> list[Task]:
    return [task for task in tasks if task.status == "blocked"]


def overdue_actions(actions: list[NextAction], today: date) -> list[NextAction]:
    return [
        action
        for action in actions
        if action.next_action_date and action.next_action_date < today
    ]
