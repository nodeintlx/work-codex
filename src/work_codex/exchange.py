from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any


EXCHANGE_DIRS = (
    "incoming",
    "outgoing",
    "handoff",
    "evidence",
    "counsel",
    "manifests",
)


def init_agent_exchange(root: Path) -> list[Path]:
    root.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for name in EXCHANGE_DIRS:
        path = root / name
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)

    _write_readme(root)
    _write_manifest_template(root)
    return created


def write_exchange_payload(root: Path, *, name: str, payload: dict[str, Any]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_exchange_manifest(
    root: Path,
    *,
    artifact_path: str,
    artifact_type: str,
    source_agent: str,
    requested_action: str,
    matter: str,
) -> Path:
    manifests_dir = root / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = manifests_dir / f"{stamp}-{artifact_type}.json"
    payload = {
        "protocol_version": "agent-exchange-manifest/v1",
        "created_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "artifact_path": artifact_path,
        "artifact_type": artifact_type,
        "source_agent": source_agent,
        "requested_action": requested_action,
        "matter": matter,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_readme(root: Path) -> None:
    path = root / "README.md"
    if path.exists():
        return
    path.write_text(
        "\n".join(
            [
                "# Agent Exchange",
                "",
                "This directory is an exchange layer for multi-agent cooperation.",
                "",
                "Rules:",
                "- Treat workspace YAML and runtime state as the source of truth.",
                "- Use `handoff/` for machine-readable exports from Codex.",
                "- Use `incoming/` for files dropped by another agent.",
                "- Use `manifests/` for machine-readable instructions describing each incoming artifact.",
                "- Do not edit case-state YAML directly from an external agent without an ingestion step.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_manifest_template(root: Path) -> None:
    path = root / "manifests" / "manifest-template.json"
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "protocol_version": "agent-exchange-manifest/v1",
                "created_at_utc": "2026-03-07T00:00:00Z",
                "artifact_path": "incoming/example.md",
                "artifact_type": "incident_memo",
                "source_agent": "claude-work-agent",
                "requested_action": "ingest_and_update_case_state",
                "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
                "codex_state_patch": {
                    "matter_status": {
                        "filing.filing_readiness": "ready_pending_lawyer",
                    },
                    "claim_updates": [
                        {
                            "id": "C3",
                            "set": {
                                "forum_track": "canada_or_cross_border",
                                "status": "ready_to_plead",
                            },
                        }
                    ],
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
