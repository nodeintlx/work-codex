from __future__ import annotations

from datetime import date
from io import StringIO
import json
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from work_codex.cli import run
from work_codex.workspace import Workspace, overdue_tasks


TASKS_YAML = """
# Active Task List
last_updated: "2026-03-06"
tasks:
  # Existing tasks
  - id: 1
    title: "Overdue task"
    company: nrg_bloom
    priority: P0
    status: todo
    due: "2026-03-01"
    notes: "Needs action"
  - id: 2
    title: "Blocked task"
    company: coldstorm
    priority: P1
    status: blocked
    due: "2026-03-08"
    notes: "Waiting"
"""

GOALS_YAML = """
quarter: "Q1 2026"
last_updated: "2026-03-02"
nrg_bloom:
  objective_1:
    title: "Secure runway"
    key_results:
      - description: "Call EDC"
        current: "Not done"
        status: at_risk
"""

PIPELINE_YAML = """
# Pipeline header
last_updated: "2026-03-02"
deals:
  - id: 1
    name: "Oando"
    company: nrg_bloom
    next_action: "Send follow-up"
    next_action_date: "2026-03-03"
    risk: low
"""

FUNDING_YAML = """
last_updated: "2026-03-02"
programs:
  - id: 1
    name: "CanExport"
    company: nrg_bloom
    next_action: "Register"
    next_action_date: "2026-03-04"
    risk: medium
"""

MEMORY_JSONL = """
{"type":"entity","name":"Makir Volcy"}
{"type":"entity","name":"NRG Bloom Inc."}
"""

CONTEXT_MD = """
# TON Infrastructure Ltd. -- Litigation Context

## Current Legal Posture

- **Phase:** 30-day good faith negotiation
- **Key deadline:** ~March 18, 2026
- **If negotiation fails:** 45-day mediation, then arbitration under Nigerian law
- **Last update:** February 22, 2026
"""

SETTLEMENT_TRACKER_YAML = """
last_updated: "2026-03-05"
matter: "NRG Bloom Inc. v. TON Infrastructure Ltd."
status: active
framework:
  mechanism: "30-day negotiation -> 45-day mediation -> arbitration"
  start_date: "2026-03-05"
  negotiation_deadline: "2026-04-04"
  mediation_deadline: "2026-05-19"
parameters:
  nrg_bloom_opening: "$727,000 USD"
  nrg_bloom_floor: "$500,000 USD"
  ton_estimated_zone: "$75K - $150K"
rounds:
  - round: 1
    date: "2026-03-05"
    assessment: "TON's position is weak."
    next_step: "Prepare filing path."
red_lines:
  - "No settlement below floor"
leverage_points:
  - name: "Axxela email trail"
    deployed: true
    impact: "Critical"
"""

MATTER_STATUS_YAML = """
matter: "NRG Bloom Inc. v. TON Infrastructure Ltd."
status: active
phase: negotiation
representation:
  mode: self_directed_with_ai
  canadian_counsel: paused
  nigerian_counsel: active
forum:
  current_track: negotiation
  canadian_path: under_evaluation
filing:
  filing_readiness: in_progress
  limitation_status: not_expired
  protective_filing_needed: to_be_determined
settlement:
  opening: "$727,000 USD"
  floor: "$500,000 USD"
next_actions:
  - "Refresh filing strategy."
notes: "Live posture overrides stale references."
last_updated: "2026-03-07"
"""


class WorkCodexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        (root / "shared").mkdir()
        (root / "knowledge").mkdir()
        (root / "src" / "work_codex").mkdir(parents=True)
        (root / "nrg-bloom" / "litigation-ton" / "tyler-macpherson").mkdir(parents=True)
        (root / "shared" / "tasks.yaml").write_text(textwrap.dedent(TASKS_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "goals.yaml").write_text(textwrap.dedent(GOALS_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "pipeline.yaml").write_text(textwrap.dedent(PIPELINE_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "funding.yaml").write_text(textwrap.dedent(FUNDING_YAML).strip() + "\n", encoding="utf-8")
        (root / "knowledge" / "memory.jsonl").write_text(textwrap.dedent(MEMORY_JSONL).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "CONTEXT.md").write_text(textwrap.dedent(CONTEXT_MD).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml").write_text(textwrap.dedent(SETTLEMENT_TRACKER_YAML).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml").write_text(textwrap.dedent(MATTER_STATUS_YAML).strip() + "\n", encoding="utf-8")
        for filename in (
            "unified-chronology.md",
            "source-linked-evidence-index.md",
            "verified-call-transcripts.md",
            "axxela-analysis.md",
            "risk-assessment.md",
            "ton-response-analysis.md",
            "master-evidence-summary-2026-02-25.md",
            "nrg-bloom-expenditure-ledger-2026-03-01.md",
            "dayo-demand-letter-to-ton.pdf",
            "ton-response-to-demand-letter.pdf",
            "ogboinbiri-site-development-agreement-signed.pdf",
            "nrg-bloom-mutual-nda-non-compete.pdf",
        ):
            (root / "nrg-bloom" / "litigation-ton" / filename).write_text("placeholder\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "tyler-macpherson" / "00000022-Joint_Venture_Agreement_NRG_BLOOM_TON_Feb_19_2025_Updated.pdf").write_text("placeholder\n", encoding="utf-8")
        self.root = root

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_validate_workspace(self) -> None:
        workspace = Workspace(self.root)
        self.assertEqual(workspace.validate(), [])
        self.assertEqual(workspace.memory_record_count(), 2)

    def test_overdue_tasks(self) -> None:
        workspace = Workspace(self.root)
        tasks = workspace.tasks()
        overdue = overdue_tasks(tasks, date(2026, 3, 7))
        self.assertEqual([task.title for task in overdue], ["Overdue task"])

    def test_status_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            exit_code = run(["--workspace", str(self.root), "status"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("overdue tasks", output)
        self.assertIn("Oando", output)
        self.assertIn("CanExport", output)

    def test_task_add_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "task-add",
                    "--title",
                    "New task",
                    "--company",
                    "nrg_bloom",
                    "--priority",
                    "P1",
                    "--due",
                    "2026-03-09",
                    "--notes",
                    "Created from CLI",
                ]
            )
        self.assertEqual(exit_code, 0)
        workspace = Workspace(self.root)
        self.assertIn("New task", [task.title for task in workspace.tasks()])
        tasks_text = (self.root / "shared" / "tasks.yaml").read_text(encoding="utf-8")
        self.assertIn("# Active Task List", tasks_text)
        self.assertIn("# Existing tasks", tasks_text)

    def test_pipeline_and_memory_mutations(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            pipeline_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "pipeline-upsert",
                    "--name",
                    "Oando",
                    "--company",
                    "nrg_bloom",
                    "--set",
                    "stage=proposal",
                    "--set",
                    "next_action_date=2026-03-08",
                ]
            )
        self.assertEqual(pipeline_code, 0)
        pipeline_text = (self.root / "shared" / "pipeline.yaml").read_text(encoding="utf-8")
        self.assertIn("# Pipeline header", pipeline_text)
        self.assertIn("stage: proposal", pipeline_text)
        self.assertIn('next_action_date: "2026-03-08"', pipeline_text)

        payload = json.dumps({"type": "entity", "name": "Test Node", "entityType": "test"})
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            memory_code = run(["--workspace", str(self.root), "memory-append", "--json", payload])
        self.assertEqual(memory_code, 0)
        memory_text = (self.root / "knowledge" / "memory.jsonl").read_text(encoding="utf-8")
        self.assertIn('"name": "Test Node"', memory_text)
        audit_text = (self.root / ".work_codex" / "audit.jsonl").read_text(encoding="utf-8")
        self.assertIn('"action": "memory_append"', audit_text)

    def test_litigation_status_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            exit_code = run(["--workspace", str(self.root), "litigation-status"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("NRG Bloom Inc. v. TON Infrastructure Ltd.", output)
        self.assertIn("Negotiation Deadline", output)
        self.assertIn("Axxela email trail", output)
        self.assertIn("self_directed_with_ai", output)
        self.assertIn("Refresh filing strategy.", output)

    def test_litigation_and_settlement_updates(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "litigation-update",
                    "--set",
                    "phase=filing_preparation",
                    "--set",
                    "forum.current_track=canadian_pre_filing",
                    "--set-json",
                    'next_actions=["Draft claim","Audit limitation"]',
                ]
            )
        self.assertEqual(code, 0)
        text = (self.root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml").read_text(encoding="utf-8")
        self.assertIn("phase: filing_preparation", text)
        self.assertIn("current_track: canadian_pre_filing", text)
        self.assertIn("- Draft claim", text)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "settlement-round-add",
                    "--json",
                    '{"date":"2026-03-07","type":"strategy_update","assessment":"Now self-directed","next_step":"Draft filing plan"}',
                ]
            )
        self.assertEqual(code, 0)
        tracker_text = (self.root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml").read_text(encoding="utf-8")
        self.assertIn("type: strategy_update", tracker_text)
        self.assertIn("next_step: Draft filing plan", tracker_text)

    def test_doctor_command(self) -> None:
        vendor_root = self.root / ".vendor" / "ruamel" / "yaml"
        vendor_root.mkdir(parents=True)
        (vendor_root / "__init__.py").write_text("# placeholder\n", encoding="utf-8")
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "doctor"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("doctor for", output)
        self.assertIn("runtime", output)
        self.assertIn("litigation matter status", output)


if __name__ == "__main__":
    unittest.main()
