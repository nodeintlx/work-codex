from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .proposals import AgentProposal, list_agent_proposals
from .workspace import Workspace


def review_queue_lines(root: Path) -> list[str]:
    proposals = list_agent_proposals(root)
    recent_ingests = _recent_ingests(root)
    review_tasks = _review_tasks(root)

    lines = [
        "agent review queue",
        f"recent ingests: {len(recent_ingests)}",
        f"pending proposals: {sum(1 for item in proposals if item.status in {'pending', 'pending_review'})}",
        f"open review tasks: {len(review_tasks)}",
    ]

    if recent_ingests:
        lines.append("recent ingested artifacts")
        for item in recent_ingests:
            lines.append(f"  - {item['artifact_type']}: {item['stored_path']}")
            lines.append(f"    source_agent: {item['source_agent']}")
            lines.append(f"    recommendation: {item['recommendation']}")

    if proposals:
        lines.append("proposal queue")
        for item in proposals:
            lines.append(f"  - [{item.status}] {item.path}")
            lines.append(f"    source_agent: {item.source_agent}")
            lines.append(f"    artifact_type: {item.artifact_type}")
            if item.supersedes:
                lines.append(f"    supersedes: {item.supersedes}")
            if item.superseded_by:
                lines.append(f"    superseded_by: {item.superseded_by}")
            if item.patch:
                lines.append("    recommendation: review and apply if the structured patch matches current case truth")
            elif item.suggested_updates:
                lines.append("    recommendation: convert the free-text suggestions into an explicit structured patch before applying")
            else:
                lines.append("    recommendation: review artifact manually before any state change")

    if review_tasks:
        lines.append("open review tasks")
        for task in review_tasks[:10]:
            due = task.due.isoformat() if task.due else "none"
            lines.append(f"  - #{task.id} {task.title} (due {due})")

    if not recent_ingests and not proposals and not review_tasks:
        lines.append("nothing pending")
    return lines


def _recent_ingests(root: Path) -> list[dict[str, Any]]:
    path = root / "knowledge" / "memory.jsonl"
    if not path.exists():
        return []
    items: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        if isinstance(data, dict) and str(data.get("type", "")) == "agent_exchange_ingest":
            items.append(data)
    items = items[-5:]
    results: list[dict[str, Any]] = []
    for item in reversed(items):
        suggestion = "review artifact and decide whether any proposal should become live state"
        proposal_path = str(item.get("proposalPath", "")).strip()
        if proposal_path:
            suggestion = "review linked proposal before applying any live-state mutation"
        results.append(
            {
                "artifact_type": str(item.get("artifactType", "")),
                "stored_path": str(item.get("storedPath", "")),
                "source_agent": str(item.get("sourceAgent", "")),
                "recommendation": suggestion,
            }
        )
    return results


def _review_tasks(root: Path):
    workspace = Workspace(root)
    return [
        task
        for task in workspace.tasks()
        if task.is_open and task.title.lower().startswith("review ingested ")
    ]
