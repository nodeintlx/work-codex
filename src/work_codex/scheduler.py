from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
import re
import time

from .filing import FilingPackage, load_filing_package
from .litigation import litigation_deadlines, load_litigation_matter
from .workspace import Task, Workspace, due_soon_tasks, overdue_tasks


@dataclass(frozen=True)
class SchedulerItem:
    source: str
    label: str
    due: date | None
    severity: str
    detail: str


@dataclass(frozen=True)
class SchedulerReport:
    generated_at: str
    items: tuple[SchedulerItem, ...]


def build_scheduler_report(root: Path, today: date) -> SchedulerReport:
    workspace = Workspace(root)
    matter = load_litigation_matter(root)
    filing = load_filing_package(root)

    items: list[SchedulerItem] = []
    litigation_tasks = [task for task in workspace.tasks() if _is_litigation_task(task)]
    for task in overdue_tasks(litigation_tasks, today):
        items.append(
            SchedulerItem(
                source="task",
                label=task.title,
                due=task.due,
                severity="critical" if task.priority == "P0" else "high",
                detail=f"Overdue workspace task for {task.company}",
            )
        )

    overdue_deadlines, upcoming_deadlines = litigation_deadlines(matter, today)
    for deadline in overdue_deadlines:
        items.append(
            SchedulerItem(
                source="litigation_deadline",
                label=deadline.label,
                due=deadline.due,
                severity="critical",
                detail=f"Deadline already passed from {deadline.source}",
            )
        )
    for deadline in upcoming_deadlines:
        items.append(
            SchedulerItem(
                source="litigation_deadline",
                label=deadline.label,
                due=deadline.due,
                severity="high",
                detail=f"Deadline within seven days from {deadline.source}",
            )
        )

    if matter.protective_filing_needed != "no":
        items.append(
            SchedulerItem(
                source="filing",
                label="Protective filing decision",
                due=today,
                severity="critical" if matter.protective_filing_needed in {"yes", "to_be_determined"} else "high",
                detail=matter.latest_next_step or "Protective filing posture still unresolved.",
            )
        )

    items.extend(_filing_scheduler_items(filing, today))

    for action in matter.live_next_actions:
        items.append(
            SchedulerItem(
                source="litigation_action",
                label=action,
                due=today,
                severity="high",
                detail="Live matter next action from matter-status.yaml",
            )
        )

    for task in due_soon_tasks(litigation_tasks, today):
        items.append(
            SchedulerItem(
                source="task",
                label=task.title,
                due=task.due,
                severity="medium",
                detail=f"Due soon workspace task for {task.company}",
            )
        )

    items.sort(key=_sort_key)
    return SchedulerReport(
        generated_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        items=tuple(items),
    )


def scheduler_lines(report: SchedulerReport) -> list[str]:
    lines = [f"scheduler report generated {report.generated_at}"]
    if not report.items:
        lines.append("  none")
        return lines
    for item in report.items:
        due = item.due.isoformat() if item.due else "none"
        lines.append(f"  [{item.severity}] {item.source}: {item.label} (due {due})")
        lines.append(f"    {item.detail}")
    return lines


def run_scheduler_loop(
    root: Path,
    *,
    today: date,
    cycles: int,
    interval_seconds: float,
) -> list[SchedulerReport]:
    reports: list[SchedulerReport] = []
    for index in range(cycles):
        report = build_scheduler_report(root, today)
        reports.append(report)
        _write_heartbeat(root, report)
        if index + 1 < cycles and interval_seconds > 0:
            time.sleep(interval_seconds)
    return reports


def _filing_scheduler_items(package: FilingPackage, today: date) -> list[SchedulerItem]:
    items: list[SchedulerItem] = []
    if package.readiness.level != "ready_for_draft":
        items.append(
            SchedulerItem(
                source="filing",
                label="Filing package readiness",
                due=today,
                severity="high" if package.readiness.level == "in_progress" else "critical",
                detail=f"Readiness is {package.readiness.level}",
            )
        )
    for recommendation in package.readiness.recommendations:
        items.append(
            SchedulerItem(
                source="filing",
                label="Filing recommendation",
                due=today,
                severity="medium",
                detail=recommendation,
            )
        )
    return items


def _write_heartbeat(root: Path, report: SchedulerReport) -> None:
    scheduler_dir = root / ".work_codex" / "scheduler"
    scheduler_dir.mkdir(parents=True, exist_ok=True)
    path = scheduler_dir / "last_run.json"
    payload = {
        "generated_at": report.generated_at,
        "items": [asdict(item) | {"due": item.due.isoformat() if item.due else None} for item in report.items],
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _sort_key(item: SchedulerItem) -> tuple[int, str, str]:
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    due = item.due.isoformat() if item.due else "9999-12-31"
    return (severity_order.get(item.severity, 9), due, item.label)


def _is_litigation_task(task: Task) -> bool:
    haystack = f"{task.title}\n{task.notes}".lower()
    phrase_keywords = (
        "statement of claim",
        "position paper",
        "calculated tactic",
        "protective filing",
    )
    if any(keyword in haystack for keyword in phrase_keywords):
        return True
    word_keywords = (
        "litigation",
        "ton",
        "dayo",
        "alberta",
        "axxela",
        "mccarthy",
        "damages",
        "arbitration",
        "mediation",
        "counterclaim",
        "evidence",
    )
    return any(re.search(rf"\b{re.escape(keyword)}\b", haystack) for keyword in word_keywords)
