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


class WorkCodexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        (root / "shared").mkdir()
        (root / "knowledge").mkdir()
        (root / "shared" / "tasks.yaml").write_text(textwrap.dedent(TASKS_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "goals.yaml").write_text(textwrap.dedent(GOALS_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "pipeline.yaml").write_text(textwrap.dedent(PIPELINE_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "funding.yaml").write_text(textwrap.dedent(FUNDING_YAML).strip() + "\n", encoding="utf-8")
        (root / "knowledge" / "memory.jsonl").write_text(textwrap.dedent(MEMORY_JSONL).strip() + "\n", encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
