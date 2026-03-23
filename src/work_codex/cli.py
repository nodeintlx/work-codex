from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys

from .actions import strategic_action_lines
from .content import (
    content_app_payload,
    calendar_lines,
    content_backend_payload,
    content_review_lines,
    content_validation_lines,
    create_content_brief,
    editorial_lines,
    generate_creative_package,
    generate_content_package,
    ingest_published_post,
    load_content_brief,
    log_post_performance,
    update_content_status,
    validate_content_brief,
    validate_content_system,
    write_content_app_payload,
    write_content_backend_payload,
)
from .doctor import summarize_doctor
from .drafting import (
    alberta_skeleton_lines,
    claim_outline_lines,
    exhibit_list_lines,
    facts_section_lines,
    write_draft_bundle,
)
from .exchange import init_agent_exchange, write_exchange_payload
from .filing import filing_outline_lines, filing_validation_errors, load_filing_package
from .handoff import build_litigation_handoff
from .ingest import ingest_exchange
from .intelligence import (
    ingest_signal,
    intelligence_backend_payload,
    route_signal,
    signal_log_lines,
    validate_intelligence_system,
    write_intelligence_backend_payload,
)
from .proposals import apply_agent_proposal, list_agent_proposals, promote_agent_proposal
from .review import review_queue_lines
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

    draft_write_bundle = subparsers.add_parser("draft-write-bundle")
    draft_write_bundle.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    litigation_next_actions = subparsers.add_parser("litigation-next-actions")
    litigation_next_actions.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    litigation_handoff = subparsers.add_parser("litigation-handoff")
    litigation_handoff.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    exchange_init = subparsers.add_parser("agent-exchange-init")
    exchange_init.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    exchange_init.add_argument("--root", required=True, help="Path to the shared exchange root")

    litigation_handoff_write = subparsers.add_parser("litigation-handoff-write")
    litigation_handoff_write.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    litigation_handoff_write.add_argument("--exchange-root", required=True, help="Path to the shared exchange root")

    exchange_ingest = subparsers.add_parser("agent-exchange-ingest")
    exchange_ingest.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    exchange_ingest.add_argument("--exchange-root", required=True, help="Path to the shared exchange root")

    proposal_status = subparsers.add_parser("agent-proposal-status")
    proposal_status.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    proposal_apply = subparsers.add_parser("agent-proposal-apply")
    proposal_apply.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    proposal_apply.add_argument("--path", required=True, help="Path to a proposal JSON file")

    proposal_promote = subparsers.add_parser("agent-proposal-promote")
    proposal_promote.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    proposal_promote.add_argument("--path", required=True, help="Path to a pending_review proposal JSON file")

    review_queue = subparsers.add_parser("agent-review-queue")
    review_queue.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

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

    content_intake = subparsers.add_parser("content-intake")
    content_intake.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_intake.add_argument("--title", required=True)
    content_intake.add_argument("--idea", required=True)
    content_intake.add_argument("--audience")
    content_intake.add_argument("--channel")
    content_intake.add_argument("--suggested-date")

    content_calendar = subparsers.add_parser("content-calendar")
    content_calendar.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    content_validate = subparsers.add_parser("content-validate")
    content_validate.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_validate.add_argument("--brief", help="Path to a YAML content brief")

    content_draft = subparsers.add_parser("content-draft")
    content_draft.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_draft.add_argument("--brief", required=True, help="Path to a YAML content brief")

    content_creative = subparsers.add_parser("content-creative")
    content_creative.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_creative.add_argument("--brief", required=True, help="Path to a YAML content brief")

    content_editorial = subparsers.add_parser("content-editorial")
    content_editorial.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    content_status = subparsers.add_parser("content-status")
    content_status.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_status.add_argument("--brief", required=True, help="Path to a YAML content brief")
    content_status.add_argument("--set-status", required=True, help="New brief workflow status")
    content_status.add_argument("--scheduled-for")
    content_status.add_argument("--published-at")

    content_backend = subparsers.add_parser("content-backend")
    content_backend.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_backend.add_argument("--write", action="store_true", help="Write backend summary JSON to the workspace")

    content_app = subparsers.add_parser("content-app")
    content_app.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_app.add_argument("--write", action="store_true", help="Write frontend contract JSON to the workspace")

    post_ingest = subparsers.add_parser("post-ingest")
    post_ingest.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    post_ingest.add_argument("--brief", required=True, help="Path to a YAML content brief")
    post_ingest.add_argument("--channel", required=True)
    post_ingest.add_argument("--body", required=True)
    post_ingest.add_argument("--posted-at", required=True)
    post_ingest.add_argument("--url")

    performance_log = subparsers.add_parser("performance-log")
    performance_log.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    performance_log.add_argument("--brief", required=True, help="Path to a YAML content brief")
    performance_log.add_argument("--channel", required=True)
    performance_log.add_argument("--captured-at", required=True)
    performance_log.add_argument("--impressions", type=int)
    performance_log.add_argument("--likes", type=int)
    performance_log.add_argument("--comments", type=int)
    performance_log.add_argument("--reposts", type=int)
    performance_log.add_argument("--saves", type=int)
    performance_log.add_argument("--profile-visits", type=int)
    performance_log.add_argument("--dms", type=int)
    performance_log.add_argument("--leads", type=int)

    content_review = subparsers.add_parser("content-review")
    content_review.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    content_review.add_argument("--brief", required=True, help="Path to a YAML content brief")

    signal_ingest = subparsers.add_parser("signal-ingest")
    signal_ingest.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    signal_ingest.add_argument("--domain", required=True)
    signal_ingest.add_argument("--headline", required=True)
    signal_ingest.add_argument("--summary", required=True)
    signal_ingest.add_argument("--nrg-angle", required=True)
    signal_ingest.add_argument("--source", required=True)
    signal_ingest.add_argument("--published-at", required=True)
    signal_ingest.add_argument("--pillar", required=True)
    signal_ingest.add_argument("--business-proximity", type=int, required=True)
    signal_ingest.add_argument("--content-opportunity", type=int, required=True)
    signal_ingest.add_argument("--recency-window", type=int, required=True)
    signal_ingest.add_argument("--topic-pillar-fit", type=int, required=True)

    signal_route = subparsers.add_parser("signal-route")
    signal_route.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    signal_route.add_argument("--id", required=True)
    signal_route.add_argument("--create-brief", action="store_true")

    signal_log = subparsers.add_parser("signal-log")
    signal_log.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    signal_backend = subparsers.add_parser("signal-backend")
    signal_backend.add_argument("--workspace", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    signal_backend.add_argument("--write", action="store_true")
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

        if args.command == "draft-write-bundle":
            root = Path(args.workspace).resolve()
            package = load_filing_package(root)
            matter = load_litigation_matter(root)
            paths = write_draft_bundle(root, package, matter)
            print("wrote draft bundle")
            for path in paths:
                print(f"- {path}")
            return 0

        if args.command == "litigation-next-actions":
            root = Path(args.workspace).resolve()
            for line in strategic_action_lines(root, today):
                print(line)
            return 0

        if args.command == "litigation-handoff":
            root = Path(args.workspace).resolve()
            payload = build_litigation_handoff(root, today)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 0

        if args.command == "agent-exchange-init":
            exchange_root = Path(args.root).expanduser().resolve()
            created = init_agent_exchange(exchange_root)
            print(f"initialized agent exchange at {exchange_root}")
            for path in created:
                print(f"- {path}")
            return 0

        if args.command == "litigation-handoff-write":
            root = Path(args.workspace).resolve()
            exchange_root = Path(args.exchange_root).expanduser().resolve()
            init_agent_exchange(exchange_root)
            payload = build_litigation_handoff(root, today)
            path = write_exchange_payload(exchange_root / "handoff", name="litigation-handoff.json", payload=payload)
            print(f"wrote litigation handoff to {path}")
            return 0

        if args.command == "agent-exchange-ingest":
            root = Path(args.workspace).resolve()
            exchange_root = Path(args.exchange_root).expanduser().resolve()
            ingested = ingest_exchange(root, exchange_root, today)
            print(f"ingested {len(ingested)} artifact(s) from {exchange_root}")
            for item in ingested:
                print(f"- {item.artifact_type}: {item.stored_artifact}")
            return 0

        if args.command == "agent-proposal-status":
            root = Path(args.workspace).resolve()
            proposals = list_agent_proposals(root)
            print(f"agent proposals: {len(proposals)}")
            for item in proposals:
                print(f"- [{item.status}] {item.path}")
                print(f"  source_agent: {item.source_agent}")
                print(f"  artifact_type: {item.artifact_type}")
                print(f"  artifact_path: {item.artifact_path}")
                if item.supersedes:
                    print(f"  supersedes: {item.supersedes}")
                if item.superseded_by:
                    print(f"  superseded_by: {item.superseded_by}")
                if item.suggested_updates:
                    print(f"  suggested_updates: {json.dumps(item.suggested_updates, sort_keys=True)}")
            return 0

        if args.command == "agent-proposal-apply":
            root = Path(args.workspace).resolve()
            proposal_path = Path(args.path).expanduser().resolve()
            applied = apply_agent_proposal(root, proposal_path, today)
            print(f"applied proposal {proposal_path}")
            for item in applied:
                print(f"- {item}")
            return 0

        if args.command == "agent-proposal-promote":
            root = Path(args.workspace).resolve()
            proposal_path = Path(args.path).expanduser().resolve()
            promoted = promote_agent_proposal(root, proposal_path, today)
            print(f"promoted proposal {proposal_path}")
            for item in promoted:
                print(f"- {item}")
            return 0

        if args.command == "agent-review-queue":
            root = Path(args.workspace).resolve()
            for line in review_queue_lines(root):
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

        if args.command == "content-intake":
            brief = create_content_brief(
                Path(args.workspace).resolve(),
                title=args.title,
                idea=args.idea,
                audience=args.audience,
                channel=args.channel,
                suggested_date=args.suggested_date,
                today=today,
            )
            print(f"captured {brief.queue_id}: {brief.title}")
            print(f"audience: {brief.audience_label}")
            print(f"pillar: {brief.pillar_label}")
            print(f"funnel stage: {brief.stage_label}")
            print(f"primary channel: {brief.primary_channel}")
            print(f"suggested publish date: {brief.suggested_publish_date}")
            print(f"cta: {brief.cta}")
            print(f"brief: {brief.brief_path}")
            return 0

        if args.command == "content-calendar":
            for line in calendar_lines(Path(args.workspace).resolve()):
                print(line)
            return 0

        if args.command == "content-validate":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve() if args.brief else None
            for line in content_validation_lines(root, brief_path):
                print(line)
            errors = validate_content_system(root)
            if brief_path is not None:
                errors.extend(validate_content_brief(load_content_brief(brief_path)))
            return 0 if not errors else 1

        if args.command == "content-draft":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve()
            package_path = generate_content_package(root, brief_path)
            print(f"wrote content draft package: {package_path}")
            return 0

        if args.command == "content-creative":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve()
            package_path = generate_creative_package(root, brief_path)
            print(f"wrote content creative package: {package_path}")
            return 0

        if args.command == "content-editorial":
            root = Path(args.workspace).resolve()
            for line in editorial_lines(root, today):
                print(line)
            return 0

        if args.command == "content-status":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve()
            updated_path, status = update_content_status(
                root,
                brief_path=brief_path,
                status=args.set_status,
                scheduled_for=args.scheduled_for,
                published_at=args.published_at,
            )
            print(f"updated content status: {status}")
            print(f"brief: {updated_path}")
            return 0

        if args.command == "content-backend":
            root = Path(args.workspace).resolve()
            if args.write:
                path = write_content_backend_payload(root, today)
                print(f"wrote content backend summary: {path}")
                return 0
            print(json.dumps(content_backend_payload(root, today), indent=2, sort_keys=True))
            return 0

        if args.command == "content-app":
            root = Path(args.workspace).resolve()
            if args.write:
                path = write_content_app_payload(root, today)
                print(f"wrote content app contract: {path}")
                return 0
            print(json.dumps(content_app_payload(root, today), indent=2, sort_keys=True))
            return 0

        if args.command == "post-ingest":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve()
            updated_path = ingest_published_post(
                root,
                brief_path=brief_path,
                channel=args.channel,
                body=args.body,
                posted_at=args.posted_at,
                url=args.url,
            )
            print(f"ingested published post: {updated_path}")
            return 0

        if args.command == "performance-log":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve()
            updated_path = log_post_performance(
                root,
                brief_path=brief_path,
                channel=args.channel,
                captured_at=args.captured_at,
                impressions=args.impressions,
                likes=args.likes,
                comments=args.comments,
                reposts=args.reposts,
                saves=args.saves,
                profile_visits=args.profile_visits,
                dms=args.dms,
                leads=args.leads,
            )
            print(f"logged post performance: {updated_path}")
            return 0

        if args.command == "content-review":
            root = Path(args.workspace).resolve()
            brief_path = Path(args.brief).expanduser().resolve()
            for line in content_review_lines(root, brief_path):
                print(line)
            return 0

        if args.command == "signal-ingest":
            root = Path(args.workspace).resolve()
            signal = ingest_signal(
                root,
                domain=args.domain,
                headline=args.headline,
                summary=args.summary,
                nrg_angle=args.nrg_angle,
                source=args.source,
                published_at=args.published_at,
                pillar=args.pillar,
                business_proximity=args.business_proximity,
                content_opportunity=args.content_opportunity,
                recency_window=args.recency_window,
                topic_pillar_fit=args.topic_pillar_fit,
            )
            print(f"ingested signal: {signal['id']}")
            print(f"headline: {signal['headline']}")
            return 0

        if args.command == "signal-route":
            root = Path(args.workspace).resolve()
            decision = route_signal(root, signal_id=args.id, create_brief=args.create_brief, today=today)
            print(f"signal {decision.signal_id}: {decision.action} ({decision.score})")
            print(f"reason: {decision.reason}")
            if decision.brief_path is not None:
                print(f"brief: {decision.brief_path}")
            return 0

        if args.command == "signal-log":
            root = Path(args.workspace).resolve()
            errors = validate_intelligence_system(root)
            if errors:
                for error in errors:
                    print(error)
                return 1
            for line in signal_log_lines(root):
                print(line)
            return 0

        if args.command == "signal-backend":
            root = Path(args.workspace).resolve()
            if args.write:
                path = write_intelligence_backend_payload(root)
                print(f"wrote intelligence backend summary: {path}")
                return 0
            print(json.dumps(intelligence_backend_payload(root), indent=2, sort_keys=True))
            return 0

        validation_errors = workspace.validate()
        if validation_errors:
            print("workspace is not ready")
            for error in validation_errors:
                print(f"- {error}")
            return 1
    except (StoreError, ValueError, json.JSONDecodeError) as exc:
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
