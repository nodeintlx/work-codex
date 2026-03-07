from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys

from .doctor import summarize_doctor
from .drafting import alberta_skeleton_lines, claim_outline_lines, exhibit_list_lines, facts_section_lines
from .filing import filing_outline_lines, filing_validation_errors, load_filing_package
from .scheduler import run_scheduler_loop, scheduler_lines
from .store import SafeWorkspaceStore, StoreError
from .litigation import artifact_gaps, context_snapshot, litigation_deadlines, load_litigation_matter
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
    for command in ("validate", "status", "followup", "doctor"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    task_add = subparsers.add_parser("task-add")
    task_add.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    task_add.add_argument("--title", required=True)
    task_add.add_argument("--company", required=True)
    task_add.add_argument("--priority", required=True)
    task_add.add_argument("--due")
    task_add.add_argument("--notes", default="")
    task_add.add_argument("--status", default="todo")
    task_add.add_argument("--created")

    task_update = subparsers.add_parser("task-update")
    task_update.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    task_update.add_argument("--id", type=int, required=True)
    task_update.add_argument("--title")
    task_update.add_argument("--company")
    task_update.add_argument("--priority")
    task_update.add_argument("--status")
    task_update.add_argument("--due")
    task_update.add_argument("--notes")
    task_update.add_argument("--append-note")

    pipeline_upsert = subparsers.add_parser("pipeline-upsert")
    pipeline_upsert.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    pipeline_upsert.add_argument("--id", type=int)
    pipeline_upsert.add_argument("--name", required=True)
    pipeline_upsert.add_argument("--company", required=True)
    pipeline_upsert.add_argument("--set", action="append", default=[])
    pipeline_upsert.add_argument("--set-json", action="append", default=[])

    funding_upsert = subparsers.add_parser("funding-upsert")
    funding_upsert.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    funding_upsert.add_argument("--id", type=int)
    funding_upsert.add_argument("--name", required=True)
    funding_upsert.add_argument("--company", required=True)
    funding_upsert.add_argument("--set", action="append", default=[])
    funding_upsert.add_argument("--set-json", action="append", default=[])

    memory_append = subparsers.add_parser("memory-append")
    memory_append.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    memory_append.add_argument("--json", required=True, help="JSON object to append as a JSONL record")

    litigation_status = subparsers.add_parser("litigation-status")
    litigation_status.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    litigation_validate = subparsers.add_parser("litigation-validate")
    litigation_validate.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    filing_status = subparsers.add_parser("filing-status")
    filing_status.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    filing_validate = subparsers.add_parser("filing-validate")
    filing_validate.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    filing_outline = subparsers.add_parser("filing-outline")
    filing_outline.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    draft_claim_outline = subparsers.add_parser("draft-claim-outline")
    draft_claim_outline.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    draft_facts = subparsers.add_parser("draft-facts")
    draft_facts.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    draft_exhibits = subparsers.add_parser("draft-exhibits")
    draft_exhibits.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    draft_alberta = subparsers.add_parser("draft-alberta-skeleton")
    draft_alberta.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    litigation_update = subparsers.add_parser("litigation-update")
    litigation_update.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    litigation_update.add_argument("--set", action="append", default=[])
    litigation_update.add_argument("--set-json", action="append", default=[])

    settlement_update = subparsers.add_parser("settlement-update")
    settlement_update.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    settlement_update.add_argument("--set", action="append", default=[])
    settlement_update.add_argument("--set-json", action="append", default=[])

    settlement_round_add = subparsers.add_parser("settlement-round-add")
    settlement_round_add.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    settlement_round_add.add_argument("--json", required=True, help="JSON object for a settlement round")

    scheduler_status = subparsers.add_parser("scheduler-status")
    scheduler_status.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    scheduler_run = subparsers.add_parser("scheduler-run")
    scheduler_run.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    scheduler_run.add_argument("--cycles", type=int, default=1)
    scheduler_run.add_argument("--interval-seconds", type=float, default=0.0)
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
    store = SafeWorkspaceStore(Path(args.workspace).resolve())
    today = date.today()

    try:
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

        if args.command == "doctor":
            ok, lines = summarize_doctor(Path(args.workspace).resolve())
            print(f"doctor for {Path(args.workspace).resolve()}")
            for line in lines:
                print(line)
            return 0 if ok else 1

        if args.command == "task-add":
            result = store.add_task(
                title=args.title,
                company=args.company,
                priority=args.priority,
                due=args.due,
                notes=args.notes,
                status=args.status,
                created=args.created,
            )
            print(result.message)
            return 0

        if args.command == "task-update":
            result = store.update_task(
                task_id=args.id,
                title=args.title,
                company=args.company,
                priority=args.priority,
                status=args.status,
                due=args.due,
                notes=args.notes,
                append_note=args.append_note,
            )
            print(result.message)
            return 0

        if args.command == "pipeline-upsert":
            result = store.upsert_pipeline(
                deal_id=args.id,
                name=args.name,
                company=args.company,
                fields=_parse_field_assignments(args.set, args.set_json),
            )
            print(result.message)
            return 0

        if args.command == "funding-upsert":
            result = store.upsert_funding(
                program_id=args.id,
                name=args.name,
                company=args.company,
                fields=_parse_field_assignments(args.set, args.set_json),
            )
            print(result.message)
            return 0

        if args.command == "memory-append":
            payload = json.loads(args.json)
            result = store.append_memory(payload)
            print(result.message)
            return 0

        if args.command == "litigation-validate":
            matter = load_litigation_matter(Path(args.workspace).resolve())
            gaps = artifact_gaps(matter)
            if gaps:
                print("litigation matter has missing artifacts")
                for gap in gaps:
                    print(f"- {gap.label}: {gap.path}")
                return 1
            print("litigation matter validation passed")
            print(f"matter: {matter.matter}")
            return 0

        if args.command == "litigation-status":
            matter = load_litigation_matter(Path(args.workspace).resolve())
            snapshot = context_snapshot(Path(args.workspace).resolve())
            overdue, upcoming = litigation_deadlines(matter, today)
            print(matter.matter)
            print(f"status: {matter.status}")
            print(f"phase: {matter.phase}")
            print(f"framework: {matter.mechanism}")
            print(f"representation mode: {matter.representation_mode}")
            print(f"canadian counsel: {matter.canadian_counsel}")
            print(f"nigerian counsel: {matter.nigerian_counsel}")
            print(f"current track: {matter.current_track}")
            print(f"canadian path: {matter.canadian_path}")
            print(f"filing readiness: {matter.filing_readiness}")
            print(f"limitation status: {matter.limitation_status}")
            print(f"protective filing needed: {matter.protective_filing_needed}")
            print(f"opening: {matter.opening}")
            print(f"floor: {matter.floor}")
            print(f"estimated TON zone: {matter.ton_zone}")
            if matter.latest_round is not None:
                print(f"latest round: {matter.latest_round} ({matter.latest_round_date.isoformat() if matter.latest_round_date else 'unknown'})")
            print(f"assessment: {matter.latest_assessment}")
            print(f"next step: {matter.latest_next_step}")
            if matter.live_next_actions:
                print("live next actions")
                for action in matter.live_next_actions:
                    print(f"  {action}")
            if matter.live_notes:
                print(f"live notes: {matter.live_notes}")
            print(f"context phase: {snapshot.get('phase', '')}")
            print(f"context key deadline: {snapshot.get('key_deadline', '')}")
            print("tracked litigation deadlines")
            for item in matter.deadlines:
                print(f"  {item.label}: {item.due.isoformat()} ({item.source})")
            print("overdue litigation deadlines")
            if not overdue:
                print("  none")
            else:
                for item in overdue:
                    print(f"  {item.label}: {item.due.isoformat()} ({item.source})")
            print("upcoming litigation deadlines")
            if not upcoming:
                print("  none")
            else:
                for item in upcoming:
                    print(f"  {item.label}: {item.due.isoformat()} ({item.source})")
            print("missing core artifacts")
            gaps = artifact_gaps(matter)
            if not gaps:
                print("  none")
            else:
                for gap in gaps:
                    print(f"  {gap.label}: {gap.path}")
            print("active leverage points")
            for point in matter.leverage_points:
                if point.get("deployed"):
                    print(f"  {point.get('name')}: {point.get('impact')}")
            return 0

        if args.command == "filing-validate":
            package = load_filing_package(Path(args.workspace).resolve())
            errors = filing_validation_errors(package)
            if errors:
                print("filing package validation failed")
                for error in errors:
                    print(f"- {error}")
                return 1
            print("filing package validation passed")
            print(f"matter: {package.matter}")
            print(f"readiness: {package.readiness.level}")
            return 0

        if args.command == "filing-status":
            package = load_filing_package(Path(args.workspace).resolve())
            errors = filing_validation_errors(package)
            print(package.matter)
            print(f"filing readiness: {package.readiness.level}")
            print(f"critical claims ready: {package.readiness.critical_claims_ready}")
            print(f"critical evidence missing: {package.readiness.critical_evidence_missing}")
            print("claims")
            for claim in package.claims:
                print(f"  [{claim.pleading_priority}] {claim.claim_id} {claim.title} ({claim.status}, {claim.forum_track})")
            print("chronology")
            for event in package.chronology:
                print(f"  {event.date} {event.event_id} {event.title}")
            print("evidence")
            for item in package.evidence:
                state = "ok" if item.exists else "missing"
                print(f"  [{state}] {item.evidence_id}: {item.path}")
            print("readiness recommendations")
            for recommendation in package.readiness.recommendations:
                print(f"  {recommendation}")
            print("validation issues")
            if not errors:
                print("  none")
            else:
                for error in errors:
                    print(f"  {error}")
            return 0

        if args.command == "filing-outline":
            package = load_filing_package(Path(args.workspace).resolve())
            for line in filing_outline_lines(package):
                print(line)
            return 0

        if args.command == "draft-claim-outline":
            package = load_filing_package(Path(args.workspace).resolve())
            for line in claim_outline_lines(package):
                print(line)
            return 0

        if args.command == "draft-facts":
            package = load_filing_package(Path(args.workspace).resolve())
            for line in facts_section_lines(package):
                print(line)
            return 0

        if args.command == "draft-exhibits":
            package = load_filing_package(Path(args.workspace).resolve())
            for line in exhibit_list_lines(package):
                print(line)
            return 0

        if args.command == "draft-alberta-skeleton":
            root = Path(args.workspace).resolve()
            package = load_filing_package(root)
            matter = load_litigation_matter(root)
            for line in alberta_skeleton_lines(package, matter):
                print(line)
            return 0

        if args.command == "litigation-update":
            result = store.update_litigation_status(_parse_field_assignments(args.set, args.set_json))
            print(result.message)
            return 0

        if args.command == "settlement-update":
            result = store.update_settlement_tracker(_parse_field_assignments(args.set, args.set_json))
            print(result.message)
            return 0

        if args.command == "settlement-round-add":
            payload = json.loads(args.json)
            result = store.append_settlement_round(payload)
            print(result.message)
            return 0

        if args.command == "scheduler-status":
            report = run_scheduler_loop(Path(args.workspace).resolve(), today=today, cycles=1, interval_seconds=0.0)[0]
            for line in scheduler_lines(report):
                print(line)
            return 0

        if args.command == "scheduler-run":
            if args.cycles < 1:
                raise StoreError("--cycles must be at least 1")
            if args.interval_seconds < 0:
                raise StoreError("--interval-seconds must be non-negative")
            reports = run_scheduler_loop(
                Path(args.workspace).resolve(),
                today=today,
                cycles=args.cycles,
                interval_seconds=args.interval_seconds,
            )
            for index, report in enumerate(reports, start=1):
                print(f"cycle {index}/{len(reports)}")
                for line in scheduler_lines(report):
                    print(line)
            return 0

        validation_errors = workspace.validate()
        if validation_errors:
            print("workspace is not ready")
            for error in validation_errors:
                print(f"- {error}")
            return 1
    except (StoreError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
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


def _parse_field_assignments(pairs: list[str], json_pairs: list[str]) -> dict[str, object]:
    fields: dict[str, object] = {}
    for pair in pairs:
        key, value = _split_assignment(pair)
        fields[key] = value
    for pair in json_pairs:
        key, raw_value = _split_assignment(pair)
        fields[key] = json.loads(raw_value)
    return fields


def _split_assignment(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise StoreError(f"expected KEY=VALUE assignment, got: {raw}")
    key, value = raw.split("=", 1)
    key = key.strip()
    if not key:
        raise StoreError(f"empty field name in assignment: {raw}")
    return key, value


if __name__ == "__main__":
    sys.exit(run())
