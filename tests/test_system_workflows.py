from __future__ import annotations

from datetime import date
from io import StringIO
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from work_codex.actions import build_strategic_actions
from work_codex.cli import run
from work_codex.drafting import write_draft_bundle
from work_codex.filing import filing_validation_errors, load_filing_package
from work_codex.litigation import load_litigation_matter
from work_codex.scheduler import build_scheduler_report


TASKS_YAML = """
last_updated: "2026-03-06"
tasks:
  - id: 1
    title: "Get Julie's written statement on calculated tactic"
    company: nrg_bloom
    priority: P1
    status: todo
    due: "2026-03-03"
    notes: "Needed for TON fight and settlement pressure."
  - id: 2
    title: "Call the bank about line of credit"
    company: nrg_bloom
    priority: P1
    status: todo
    due: "2026-03-03"
    notes: "General finance item, unrelated to dispute work."
  - id: 3
    title: "Obtain full 2022 complaint and Phoenix Trading outcome"
    company: nrg_bloom
    priority: P2
    status: todo
    due: "2026-03-06"
    notes: "Pattern evidence for TON dispute."
"""

GOALS_YAML = """
quarter: "Q1 2026"
last_updated: "2026-03-02"
nrg_bloom:
  objective_1:
    title: "Win TON settlement"
    key_results:
      - description: "Prepare filing package"
        current: "In progress"
        status: at_risk
"""

PIPELINE_YAML = """
last_updated: "2026-03-02"
deals:
  - id: 1
    name: "General Deal"
    company: nrg_bloom
    next_action: "Follow up"
    next_action_date: "2026-03-03"
    risk: low
"""

FUNDING_YAML = """
last_updated: "2026-03-02"
programs:
  - id: 1
    name: "General Grant"
    company: nrg_bloom
    next_action: "Submit form"
    next_action_date: "2026-03-04"
    risk: medium
"""

MEMORY_JSONL = """
{"type":"entity","name":"Makir Volcy"}
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
last_updated: "2026-03-07"
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
phase: filing_strategy
representation:
  mode: self_directed_with_ai
  canadian_counsel: paused
  nigerian_counsel: active
forum:
  current_track: negotiation_plus_canadian_pre_filing
  canadian_path: under_active_evaluation
filing:
  filing_readiness: in_progress
  limitation_status: not_expired
  protective_filing_needed: to_be_determined
settlement:
  opening: "$727,000 USD"
  floor: "$500,000 USD"
next_actions:
  - "Decide whether to prepare a protective Alberta filing package now."
notes: "Live posture overrides stale references."
last_updated: "2026-03-07"
"""

CLAIMS_MAP_YAML = """
last_updated: "2026-03-07"
matter: "NRG Bloom Inc. v. TON Infrastructure Ltd."
claims:
  - id: C1
    title: Bad-faith termination
    forum_track: nigeria_primary
    status: ready_to_plead
    pleading_priority: critical
    remedy_objective: Damages
    theory: TON used termination as a takeover tool.
    key_facts:
      - Funding refusal preceded deterioration.
    evidence_ids:
      - E-SIGNED-SDA
      - E-CALL-TRANSCRIPTS
    chronology_event_ids:
      - CH1
    damages_anchor: Contract and conduct support damages.
    pleading_notes: Start with termination sequence.
  - id: C2
    title: Axxela circumvention
    forum_track: canada_or_cross_border
    status: ready_to_plead
    pleading_priority: critical
    remedy_objective: Preserve leverage
    theory: TON excluded NRG Bloom from Axxela.
    key_facts:
      - NRG Bloom originated the opportunity.
    evidence_ids:
      - E-EMAIL-TIMELINE
      - E-MNDA
    chronology_event_ids:
      - CH2
    damages_anchor: Main leverage claim.
    pleading_notes: Preserve exact exclusion dates.
  - id: C3
    title: Misrepresentation to Axxela
    forum_track: nigeria_primary
    status: needs_forum_review
    pleading_priority: high
    remedy_objective: Add pressure
    theory: TON misrepresented NRG Bloom's knowledge.
    key_facts:
      - July 4 statement is inconsistent with NRG Bloom's position.
    evidence_ids:
      - E-EMAIL-TIMELINE
    chronology_event_ids:
      - CH2
    damages_anchor: Credibility and leverage.
    pleading_notes: Confirm forum.
  - id: C4
    title: Unjust enrichment
    forum_track: nigeria_primary
    status: in_progress
    pleading_priority: high
    remedy_objective: Capture unpaid work value
    theory: NRG Bloom provided unpaid operational work.
    key_facts:
      - NRG Bloom supported site operations.
    evidence_ids:
      - E-EXPENDITURE-LEDGER
    chronology_event_ids:
      - CH1
    damages_anchor: Needs quantified schedule.
    pleading_notes: Tighten damages schedule.
"""

CHRONOLOGY_MAP_YAML = """
last_updated: "2026-03-07"
matter: "NRG Bloom Inc. v. TON Infrastructure Ltd."
events:
  - id: CH1
    date: "2025-05-16"
    phase: restructuring
    title: SDA signed
    significance: Contract anchor.
    evidence_ids:
      - E-SIGNED-SDA
  - id: CH2
    date: "2025-07-04"
    phase: circumvention
    title: Direct-arrangement statement to Axxela
    significance: Main misrepresentation anchor.
    evidence_ids:
      - E-EMAIL-TIMELINE
"""

EVIDENCE_MAP_YAML = """
last_updated: "2026-03-07"
matter: "NRG Bloom Inc. v. TON Infrastructure Ltd."
evidence:
  - id: E-SIGNED-SDA
    title: Signed SDA
    source_type: document
    path: ogboinbiri-site-development-agreement-signed.pdf
    strength: critical
    issues:
      - contract
  - id: E-CALL-TRANSCRIPTS
    title: Call transcripts
    source_type: analysis
    path: verified-call-transcripts.md
    strength: critical
    issues:
      - admissions
  - id: E-EMAIL-TIMELINE
    title: Email timeline
    source_type: analysis
    path: master-verified-email-timeline-2025.md
    strength: critical
    issues:
      - axxela
  - id: E-MNDA
    title: MNDA
    source_type: document
    path: nrg-bloom-mutual-nda-non-compete.pdf
    strength: critical
    issues:
      - non_circumvention
  - id: E-EXPENDITURE-LEDGER
    title: Expenditure ledger
    source_type: analysis
    path: nrg-bloom-expenditure-ledger-2026-03-01.md
    strength: medium
    issues:
      - damages
"""


class SystemWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "shared").mkdir()
        (self.root / "knowledge").mkdir()
        (self.root / "nrg-bloom" / "litigation-ton" / "tyler-macpherson").mkdir(parents=True)
        self._write("shared/tasks.yaml", TASKS_YAML)
        self._write("shared/goals.yaml", GOALS_YAML)
        self._write("shared/pipeline.yaml", PIPELINE_YAML)
        self._write("shared/funding.yaml", FUNDING_YAML)
        self._write("knowledge/memory.jsonl", MEMORY_JSONL)
        self._write("nrg-bloom/litigation-ton/CONTEXT.md", CONTEXT_MD)
        self._write("nrg-bloom/litigation-ton/settlement-tracker.yaml", SETTLEMENT_TRACKER_YAML)
        self._write("nrg-bloom/litigation-ton/matter-status.yaml", MATTER_STATUS_YAML)
        self._write("nrg-bloom/litigation-ton/claims-map.yaml", CLAIMS_MAP_YAML)
        self._write("nrg-bloom/litigation-ton/chronology-map.yaml", CHRONOLOGY_MAP_YAML)
        self._write("nrg-bloom/litigation-ton/evidence-map.yaml", EVIDENCE_MAP_YAML)
        for filename in (
            "unified-chronology.md",
            "source-linked-evidence-index.md",
            "verified-call-transcripts.md",
            "axxela-analysis.md",
            "risk-assessment.md",
            "ton-response-analysis.md",
            "master-evidence-summary-2026-02-25.md",
            "nrg-bloom-expenditure-ledger-2026-03-01.md",
            "master-verified-email-timeline-2025.md",
            "ton-position-summary-counter-analysis-2026-03-05.md",
            "ton-narrative-and-counterarguments.md",
            "dayo-demand-letter-to-ton.pdf",
            "ton-response-to-demand-letter.pdf",
            "ogboinbiri-site-development-agreement-signed.pdf",
            "nrg-bloom-mutual-nda-non-compete.pdf",
        ):
            self._write(f"nrg-bloom/litigation-ton/{filename}", "placeholder\n")
        self._write(
            "nrg-bloom/litigation-ton/tyler-macpherson/00000022-Joint_Venture_Agreement_NRG_BLOOM_TON_Feb_19_2025_Updated.pdf",
            "placeholder\n",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_filing_validation_catches_missing_cross_references(self) -> None:
        broken_claims = CLAIMS_MAP_YAML.replace("E-MNDA", "E-NOT-REAL")
        self._write("nrg-bloom/litigation-ton/claims-map.yaml", broken_claims)

        package = load_filing_package(self.root)
        errors = filing_validation_errors(package)

        self.assertTrue(any("C2 references missing evidence id: E-NOT-REAL" in error for error in errors))

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "filing-validate"])
        self.assertEqual(exit_code, 1)
        self.assertIn("validation failed", stdout.getvalue())
        self.assertIn("E-NOT-REAL", stdout.getvalue())

    def test_scheduler_filters_non_litigation_work_and_keeps_case_pressure_items(self) -> None:
        report = build_scheduler_report(self.root, date(2026, 3, 7))
        labels = [item.label for item in report.items]

        self.assertIn("Get Julie's written statement on calculated tactic", labels)
        self.assertIn("Protective filing decision", labels)
        self.assertNotIn("Call the bank about line of credit", labels)
        self.assertTrue(any(item.source == "litigation_deadline" for item in report.items))

    def test_strategic_actions_align_with_bundle_outputs(self) -> None:
        actions = build_strategic_actions(self.root, date(2026, 3, 7))
        titles = [action.title for action in actions]

        self.assertIn("Decide and prepare the protective Alberta filing path", titles)
        self.assertIn("Resolve forum treatment for the Axxela misrepresentation count", titles)
        self.assertIn("Quantify the unjust-enrichment and operations damages schedule", titles)

        package = load_filing_package(self.root)
        matter = load_litigation_matter(self.root)
        written_paths = write_draft_bundle(self.root, package, matter)
        latest_dir = self.root / "nrg-bloom" / "litigation-ton" / "generated" / "latest"
        next_actions_text = (latest_dir / "next-actions.md").read_text(encoding="utf-8")
        alberta_text = (latest_dir / "alberta-protective-skeleton.md").read_text(encoding="utf-8")

        self.assertEqual(len(written_paths), 5)
        for title in titles:
            self.assertIn(title, next_actions_text)
        self.assertIn("Axxela circumvention", alberta_text)

    def test_cli_routes_commands_to_correct_subsystems(self) -> None:
        with patch("work_codex.cli.strategic_action_lines", return_value=["strategy-line"]) as action_lines:
            stdout = StringIO()
            with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
                mocked_date.today.return_value = date(2026, 3, 7)
                exit_code = run(["--workspace", str(self.root), "litigation-next-actions"])
            self.assertEqual(exit_code, 0)
            action_lines.assert_called_once()
            self.assertIn("strategy-line", stdout.getvalue())

        fake_path = self.root / "nrg-bloom" / "litigation-ton" / "generated" / "latest" / "claim-outline.md"
        with patch("work_codex.cli.write_draft_bundle", return_value=[fake_path]) as bundle_writer:
            stdout = StringIO()
            with patch("sys.stdout", stdout):
                exit_code = run(["--workspace", str(self.root), "draft-write-bundle"])
            self.assertEqual(exit_code, 0)
            bundle_writer.assert_called_once()
            self.assertIn("wrote draft bundle", stdout.getvalue())
            self.assertIn(str(fake_path), stdout.getvalue())

    def _write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
