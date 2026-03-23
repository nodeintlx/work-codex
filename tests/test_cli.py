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
from work_codex.proposals import supersede_matching_proposals
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
"""


class WorkCodexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        (root / "shared").mkdir()
        (root / "knowledge").mkdir()
        (root / "src" / "work_codex").mkdir(parents=True)
        (root / "nrg-bloom" / "litigation-ton" / "tyler-macpherson").mkdir(parents=True)
        (root / "nrg-bloom" / "marketing" / "ideas").mkdir(parents=True)
        (root / "shared" / "tasks.yaml").write_text(textwrap.dedent(TASKS_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "goals.yaml").write_text(textwrap.dedent(GOALS_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "pipeline.yaml").write_text(textwrap.dedent(PIPELINE_YAML).strip() + "\n", encoding="utf-8")
        (root / "shared" / "funding.yaml").write_text(textwrap.dedent(FUNDING_YAML).strip() + "\n", encoding="utf-8")
        (root / "knowledge" / "memory.jsonl").write_text(textwrap.dedent(MEMORY_JSONL).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "CONTEXT.md").write_text(textwrap.dedent(CONTEXT_MD).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml").write_text(textwrap.dedent(SETTLEMENT_TRACKER_YAML).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml").write_text(textwrap.dedent(MATTER_STATUS_YAML).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "claims-map.yaml").write_text(textwrap.dedent(CLAIMS_MAP_YAML).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "chronology-map.yaml").write_text(textwrap.dedent(CHRONOLOGY_MAP_YAML).strip() + "\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "evidence-map.yaml").write_text(textwrap.dedent(EVIDENCE_MAP_YAML).strip() + "\n", encoding="utf-8")
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
            (root / "nrg-bloom" / "litigation-ton" / filename).write_text("placeholder\n", encoding="utf-8")
        (root / "nrg-bloom" / "litigation-ton" / "tyler-macpherson" / "00000022-Joint_Venture_Agreement_NRG_BLOOM_TON_Feb_19_2025_Updated.pdf").write_text("placeholder\n", encoding="utf-8")
        (root / "nrg-bloom" / "marketing" / "brand-system.yaml").write_text(
            textwrap.dedent(
                """
                last_updated: "2026-03-10"
                audiences:
                  founders:
                    label: "Cross-border founders"
                    pain_points:
                      - "They confuse contribution with leverage."
                  diaspora_founders:
                    label: "Diaspora founders building in Africa"
                    pain_points:
                      - "They want to build back home without losing control."
                  energy_infrastructure_partners:
                    label: "Energy and infrastructure partners"
                    pain_points:
                      - "They care about credible operators."
                  investors:
                    label: "Investors"
                    pain_points:
                      - "They want disciplined operators."
                content_pillars:
                  builder_credibility:
                    label: "Builder credibility"
                    outcomes:
                      - "Prove operating experience."
                  nigeria_market_reality:
                    label: "Nigeria market reality"
                    outcomes:
                      - "Show practical ground truth."
                  founder_lessons:
                    label: "Founder lessons"
                    outcomes:
                      - "Turn mistakes into authority."
                  future_facing_authority:
                    label: "Future-facing authority"
                    outcomes:
                      - "Stay focused on the next build."
                funnel:
                  awareness:
                    label: "Top of funnel"
                    default_cta: "Follow NRG Bloom for practical lessons."
                    lead_magnet: "Field Notes memo"
                    recommended_assets:
                      - "LinkedIn founder post"
                  consideration:
                    label: "Middle of funnel"
                    default_cta: "Reply 'checklist' if you want the checklist."
                    lead_magnet: "Operator checklist"
                    recommended_assets:
                      - "Framework post"
                  decision:
                    label: "Bottom of funnel"
                    default_cta: "DM NRG Bloom if you're evaluating a project."
                    lead_magnet: "Project diagnostic call"
                    recommended_assets:
                      - "Offer post"
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (root / "nrg-bloom" / "marketing" / "content-brief-schema-2026-03-10.md").write_text(
            "# Content Brief Schema\n",
            encoding="utf-8",
        )
        (root / "nrg-bloom" / "marketing" / "library").mkdir(parents=True)
        (root / "nrg-bloom" / "marketing" / "library" / "exemplars.yaml").write_text(
            textwrap.dedent(
                """
                last_updated: "2026-03-10"
                library:
                  exemplars:
                    - id: "EX-001"
                      name: "Builder Positioning"
                      format: "linkedin"
                      pillars:
                        - "builder_credibility"
                        - "founder_lessons"
                      stages:
                        - "awareness"
                      opening_pattern: "Start with quiet authority. Contrast polished narrative with hard execution."
                      moves:
                        - "Use short stand-alone lines to build rhythm."
                        - "Name unseen work before naming the lesson."
                      closing_pattern: "Close by inviting the audience into future lessons, not by forcing a sale."
                    - id: "EX-002"
                      name: "Nigeria Execution Insight"
                      format: "linkedin"
                      pillars:
                        - "nigeria_market_reality"
                      stages:
                        - "awareness"
                      opening_pattern: "Open with a misconception, then replace it with ground truth."
                      moves:
                        - "State what outsiders usually miss."
                        - "Translate the issue into trust, timing, or local execution."
                      closing_pattern: "End on a practical takeaway that changes how builders should move."
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (root / "nrg-bloom" / "marketing" / "content-queue.yaml").write_text(
            textwrap.dedent(
                """
                last_updated: "2026-03-10"
                cadence:
                  weekly_posts: 3
                  publish_days:
                    - "Tuesday"
                    - "Thursday"
                    - "Friday"
                items:
                  - id: "CM-001"
                    brief_id: "CB-000"
                    status: planned
                    scheduled_for: "2026-03-12"
                    title: "What a year of hard execution taught me"
                    pillar: builder_credibility
                    audience: founders
                    funnel_stage: awareness
                    primary_channel: linkedin
                    repurpose_channels:
                      - x
                      - email
                    cta: "Follow NRG Bloom for practical lessons."
                    lead_magnet: "Field Notes memo"
                    brief_path: "nrg-bloom/marketing/briefs/cb-000-hard-execution.yaml"
                    note_path: "nrg-bloom/marketing/ideas/2026-03-12-hard-execution.md"
                    source: "seed"
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (root / "nrg-bloom" / "marketing" / "briefs").mkdir(parents=True)
        (root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml").write_text(
            textwrap.dedent(
                """
                id: "CB-001"
                created_at: "2026-03-10"
                updated_at: "2026-03-10"
                status: "approved_for_drafting"
                owner: "makir"
                source_type: "founder_idea"
                source_ref: "manual_intake"
                title: "Why physical movement matters in Nigerian project execution"
                raw_idea: "Founders from Canada often assume meetings and slide decks are enough, but in Nigeria people need to see visible progress, local presence, and movement before trust compounds."
                audience:
                  primary: "diaspora_founders"
                content_pillar: "nigeria_market_reality"
                funnel_stage: "awareness"
                campaign_theme: "building in West Africa"
                business_goal: "Strengthen founder authority."
                primary_cta: "Follow NRG Bloom for practical lessons."
                lead_magnet: "Field Notes memo"
                main_thesis: "In Nigeria, trust compounds through visible movement, not just meetings and planning."
                punch_idea: "If people cannot see movement, they assume nothing is real."
                contrarian_angle: "What looks like a communication problem is often a visibility problem."
                emotional_driver: "hard-won credibility"
                proof_points:
                  - "Visible action builds trust."
                hooks:
                  - "Most founders think updates build trust. In Nigeria, visible movement does."
                  - "If your project only exists in calls and decks, many stakeholders will treat it as unreal."
                  - "One of the most expensive cross-border lessons: trust needs to be seen."
                supporting_points:
                  - "Physical presence changes stakeholder confidence."
                  - "Visible action reduces doubt faster than explanation."
                  - "Execution culture varies by market."
                objections_to_answer:
                  - "Is this just a communication issue?"
                  - "Can remote teams solve this with better reporting?"
                closing_angle: "Serious operators design for local trust mechanics."
                primary_format: "linkedin_post"
                primary_channel: "linkedin"
                repurpose_formats:
                  - "x_thread"
                  - "email_note"
                  - "short_video_script"
                series_role: "pillar_builder"
                publish_window: "2026-03-19"
                creative_direction:
                  visual_theme: "field realism"
                guardrails:
                  legal_risk_level: "safe_public_generic"
                drafts:
                  linkedin: ""
                  x_thread: ""
                  email: ""
                  article_outline: ""
                  video_script: ""
                  faq: ""
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
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

    def test_content_intake_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            exit_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-intake",
                    "--title",
                    "What people misunderstand about building in Nigeria",
                    "--idea",
                    "Founders underestimate how much trust, logistics, and visible movement matter when executing real infrastructure projects in Nigeria.",
                ]
            )
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("captured CM-002", output)
        self.assertIn("brief: ", output)
        self.assertIn("Nigeria market reality", output)
        idea_path = self.root / "nrg-bloom" / "marketing" / "ideas" / "2026-03-13-what-people-misunderstand-about-building-in-nigeria.md"
        self.assertTrue(idea_path.exists())
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-002-what-people-misunderstand-about-building-in-nigeria.yaml"
        self.assertTrue(brief_path.exists())
        brief_text = brief_path.read_text(encoding="utf-8")
        self.assertIn("id: CB-002", brief_text)
        self.assertIn("status: drafting_ready", brief_text)
        self.assertIn("primary_format: linkedin_post", brief_text)
        queue_text = (self.root / "nrg-bloom" / "marketing" / "content-queue.yaml").read_text(encoding="utf-8")
        self.assertIn("CM-002", queue_text)
        self.assertIn("brief_id: CB-002", queue_text)
        self.assertIn("diaspora_founders", queue_text)

    def test_content_calendar_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "content-calendar"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("NRG Bloom content calendar", output)
        self.assertIn("CM-001", output)

    def test_content_validate_command(self) -> None:
        stdout = StringIO()
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml"
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "content-validate", "--brief", str(brief_path)])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("system: ok", output)
        self.assertIn("brief cb-001.yaml: ok", output)

    def test_content_draft_command(self) -> None:
        stdout = StringIO()
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml"
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "content-draft", "--brief", str(brief_path)])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("wrote content draft package", output)
        package_path = self.root / "nrg-bloom" / "marketing" / "generated" / "cb-001-drafts.md"
        self.assertTrue(package_path.exists())
        package_text = package_path.read_text(encoding="utf-8")
        self.assertIn("## Linkedin", package_text)
        self.assertIn("## Video Script", package_text)
        self.assertIn("Most people see the headline. Operators see the constraint.", package_text)
        brief_text = brief_path.read_text(encoding="utf-8")
        self.assertIn("drafts:", brief_text)
        self.assertIn("Follow NRG Bloom for practical lessons.", brief_text)

    def test_content_creative_command(self) -> None:
        stdout = StringIO()
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml"
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "content-creative", "--brief", str(brief_path)])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("wrote content creative package", output)
        package_path = self.root / "nrg-bloom" / "marketing" / "generated" / "cb-001-creative.md"
        self.assertTrue(package_path.exists())
        package_text = package_path.read_text(encoding="utf-8")
        self.assertIn("## Thumbnail Concepts", package_text)
        self.assertIn("## Short Video Storyboard", package_text)

    def test_post_ingest_performance_log_and_review(self) -> None:
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml"
        run(["--workspace", str(self.root), "content-draft", "--brief", str(brief_path)])

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "post-ingest",
                    "--brief",
                    str(brief_path),
                    "--channel",
                    "linkedin",
                    "--body",
                    "This is the final post I actually published on LinkedIn.",
                    "--posted-at",
                    "2026-03-11",
                    "--url",
                    "https://www.linkedin.com/feed/update/test",
                ]
            )
        self.assertEqual(exit_code, 0)
        self.assertIn("ingested published post", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "performance-log",
                    "--brief",
                    str(brief_path),
                    "--channel",
                    "linkedin",
                    "--captured-at",
                    "2026-03-11",
                    "--impressions",
                    "1200",
                    "--likes",
                    "44",
                    "--comments",
                    "9",
                    "--reposts",
                    "3",
                    "--saves",
                    "5",
                    "--profile-visits",
                    "18",
                    "--dms",
                    "2",
                    "--leads",
                    "1",
                ]
            )
        self.assertEqual(exit_code, 0)
        self.assertIn("logged post performance", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "content-review", "--brief", str(brief_path)])
        self.assertEqual(exit_code, 0)
        review_text = stdout.getvalue()
        self.assertIn("BloomFlow review: CB-001", review_text)
        self.assertIn("changed: yes", review_text)
        self.assertIn("impressions: 1200", review_text)
        self.assertIn("leads: 1", review_text)

        brief_text = brief_path.read_text(encoding="utf-8")
        self.assertIn("published_posts:", brief_text)
        self.assertIn("performance_snapshots:", brief_text)

    def test_content_editorial_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            exit_code = run(["--workspace", str(self.root), "content-editorial"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("BloomFlow editorial board", output)
        self.assertIn("funnel coverage", output)
        self.assertIn("editorial gaps", output)

    def test_content_status_command(self) -> None:
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml"
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            review_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-status",
                    "--brief",
                    str(brief_path),
                    "--set-status",
                    "in_review",
                ]
            )
        self.assertEqual(review_code, 0)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            approve_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-status",
                    "--brief",
                    str(brief_path),
                    "--set-status",
                    "approved",
                ]
            )
        self.assertEqual(approve_code, 0)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-status",
                    "--brief",
                    str(brief_path),
                    "--set-status",
                    "scheduled",
                    "--scheduled-for",
                    "2026-03-18",
                ]
            )
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("updated content status: scheduled", output)
        brief_text = brief_path.read_text(encoding="utf-8")
        self.assertIn("status: scheduled", brief_text)
        self.assertIn("publish_window: '2026-03-18'", brief_text)

    def test_content_status_rejects_invalid_transition(self) -> None:
        stdout = StringIO()
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-001.yaml"
        with patch("sys.stdout", stdout):
            exit_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-status",
                    "--brief",
                    str(brief_path),
                    "--set-status",
                    "published",
                ]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("invalid status transition", stdout.getvalue())

    def test_content_backend_command(self) -> None:
        queue_path = self.root / "nrg-bloom" / "marketing" / "content-queue.yaml"
        queue_text = queue_path.read_text(encoding="utf-8")
        queue_path.write_text(queue_text.replace("status: planned", "status: approved", 1), encoding="utf-8")
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-000-hard-execution.yaml"
        brief_path.write_text(
            textwrap.dedent(
                """
                id: "CB-000"
                status: "scheduled"
                drafts:
                  linkedin: "Draft present"
                creative_direction:
                  visual_theme: "operator realism"
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            exit_code = run(["--workspace", str(self.root), "content-backend"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        payload = json.loads(output)
        self.assertEqual(payload["agent_name"], "BloomFlow")
        self.assertIn("summary", payload)
        self.assertIn("items", payload)
        item = payload["items"][0]
        self.assertEqual(item["status"], "scheduled")
        self.assertEqual(item["queue_status"], "approved")
        self.assertEqual(item["brief_status"], "scheduled")
        self.assertTrue(item["has_drafts"])
        self.assertTrue(item["has_creative"])

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            exit_code = run(["--workspace", str(self.root), "content-backend", "--write"])
        self.assertEqual(exit_code, 0)
        backend_path = self.root / "nrg-bloom" / "marketing" / "generated" / "backend-summary.json"
        self.assertTrue(backend_path.exists())

    def test_content_app_command(self) -> None:
        queue_path = self.root / "nrg-bloom" / "marketing" / "content-queue.yaml"
        queue_text = queue_path.read_text(encoding="utf-8")
        queue_path.write_text(queue_text.replace("status: planned", "status: approved", 1), encoding="utf-8")
        brief_path = self.root / "nrg-bloom" / "marketing" / "briefs" / "cb-000-hard-execution.yaml"
        brief_path.write_text(
            textwrap.dedent(
                """
                id: "CB-000"
                status: "scheduled"
                drafts:
                  linkedin: "Draft present"
                creative_direction:
                  visual_theme: "operator realism"
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            exit_code = run(["--workspace", str(self.root), "content-app"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        payload = json.loads(output)
        self.assertEqual(payload["agent"]["name"], "BloomFlow")
        self.assertIn("views", payload)
        self.assertIn("actions", payload)
        card = payload["views"]["dashboard"]["cards"][0]
        self.assertEqual(card["status"], "scheduled")
        detail = next(iter(payload["views"]["brief_detail"].values()))
        self.assertEqual(detail["status"], "scheduled")
        self.assertEqual(detail["queue_status"], "approved")
        self.assertEqual(detail["brief_status"], "scheduled")

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            exit_code = run(["--workspace", str(self.root), "content-app", "--write"])
        self.assertEqual(exit_code, 0)
        app_path = self.root / "nrg-bloom" / "marketing" / "generated" / "app-contract.json"
        self.assertTrue(app_path.exists())

    def test_signal_ingest_and_route_commands(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            ingest_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "signal-ingest",
                    "--domain",
                    "ai_infra",
                    "--headline",
                    "Hyperscaler expands African data center footprint",
                    "--summary",
                    "A hyperscaler announced a major new African data center expansion tied to AI demand.",
                    "--nrg-angle",
                    "NRG Bloom can comment on modular infrastructure and local execution reality.",
                    "--source",
                    "Datacenter Dynamics",
                    "--published-at",
                    "2026-03-10",
                    "--pillar",
                    "future_facing_authority",
                    "--business-proximity",
                    "9",
                    "--content-opportunity",
                    "9",
                    "--recency-window",
                    "10",
                    "--topic-pillar-fit",
                    "9",
                ]
            )
        self.assertEqual(ingest_code, 0)
        self.assertIn("ingested signal: SIG-001", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 10)
            route_code = run(
                [
                    "--workspace",
                    str(self.root),
                    "signal-route",
                    "--id",
                    "SIG-001",
                    "--create-brief",
                ]
            )
        output = stdout.getvalue()
        self.assertEqual(route_code, 0)
        self.assertIn("ADVISORY", output)
        self.assertIn("brief:", output)
        signal_log_path = self.root / "nrg-bloom" / "marketing" / "intelligence" / "signal-log.jsonl"
        self.assertTrue(signal_log_path.exists())
        queue_text = (self.root / "nrg-bloom" / "marketing" / "content-queue.yaml").read_text(encoding="utf-8")
        self.assertIn("CM-002", queue_text)

    def test_signal_backend_command(self) -> None:
        run(
            [
                "--workspace",
                str(self.root),
                "signal-ingest",
                "--domain",
                "manual",
                "--headline",
                "Manual operator insight",
                "--summary",
                "Operators in Nigeria see the problem earlier than financiers do.",
                "--nrg-angle",
                "NRG Bloom can frame this as field-tested operator truth.",
                "--source",
                "manual",
                "--published-at",
                "2026-03-10",
                "--pillar",
                "builder_credibility",
                "--business-proximity",
                "8",
                "--content-opportunity",
                "8",
                "--recency-window",
                "8",
                "--topic-pillar-fit",
                "8",
            ]
        )
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "signal-backend"])
        self.assertEqual(exit_code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["agent_name"], "BloomFlow")
        self.assertEqual(len(payload["signals"]), 1)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            exit_code = run(["--workspace", str(self.root), "signal-backend", "--write"])
        self.assertEqual(exit_code, 0)
        backend_path = self.root / "nrg-bloom" / "marketing" / "generated" / "intelligence-summary.json"
        self.assertTrue(backend_path.exists())

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

    def test_filing_commands(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            status_code = run(["--workspace", str(self.root), "filing-status"])
        output = stdout.getvalue()
        self.assertEqual(status_code, 0)
        self.assertIn("filing readiness", output)
        self.assertIn("C1 Bad-faith termination", output)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            validate_code = run(["--workspace", str(self.root), "filing-validate"])
        self.assertEqual(validate_code, 0)
        self.assertIn("validation passed", stdout.getvalue())

    def test_draft_commands(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "draft-claim-outline"])
        self.assertEqual(code, 0)
        self.assertIn("Claim Outline", stdout.getvalue())
        self.assertIn("Bad-faith termination", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "draft-facts"])
        self.assertEqual(code, 0)
        self.assertIn("Draft Facts Section", stdout.getvalue())
        self.assertIn("2025-05-16 - SDA signed", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "draft-exhibits"])
        self.assertEqual(code, 0)
        self.assertIn("Exhibit 1", stdout.getvalue())
        self.assertIn("ogboinbiri-site-development-agreement-signed.pdf", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "draft-alberta-skeleton"])
        self.assertEqual(code, 0)
        self.assertIn("Protective Alberta Filing Skeleton", stdout.getvalue())
        self.assertIn("Court of King's Bench of Alberta", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "draft-write-bundle"])
        self.assertEqual(code, 0)
        self.assertIn("wrote draft bundle", stdout.getvalue())
        latest_dir = self.root / "nrg-bloom" / "litigation-ton" / "generated" / "latest"
        self.assertTrue((latest_dir / "claim-outline.md").exists())
        self.assertTrue((latest_dir / "next-actions.md").exists())

    def test_litigation_next_actions_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(["--workspace", str(self.root), "litigation-next-actions"])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("strategic actions", output)
        self.assertIn("settlement", output.lower())

    def test_litigation_handoff_command(self) -> None:
        incident_memo = self.root / "nrg-bloom" / "litigation-ton" / "incident-memo-test-2026-03-07.md"
        incident_memo.write_text("# Incident Memo\n", encoding="utf-8")
        generated_latest = self.root / "nrg-bloom" / "litigation-ton" / "generated" / "latest"
        generated_latest.mkdir(parents=True)
        (generated_latest / "next-actions.md").write_text("# Next Actions\n", encoding="utf-8")

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(["--workspace", str(self.root), "litigation-handoff"])

        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["protocol_version"], "law-agent-handoff/v1")
        self.assertEqual(payload["matter"]["name"], "NRG Bloom Inc. v. TON Infrastructure Ltd.")
        self.assertEqual(payload["strategy"]["top_action"]["title"], "Decide and prepare the protective Alberta filing path")
        self.assertIn("nrg-bloom/litigation-ton/incident-memo-test-2026-03-07.md", payload["artifacts"]["latest_incident_memos"])

    def test_agent_exchange_commands(self) -> None:
        exchange_root = self.root / "agent-exchange"

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "agent-exchange-init", "--root", str(exchange_root)])
        self.assertEqual(code, 0)
        self.assertTrue((exchange_root / "handoff").exists())
        self.assertTrue((exchange_root / "manifests" / "manifest-template.json").exists())

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "litigation-handoff-write",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        handoff_path = exchange_root / "handoff" / "litigation-handoff.json"
        self.assertTrue(handoff_path.exists())
        payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["protocol_version"], "law-agent-handoff/v1")

        incoming_dir = exchange_root / "incoming"
        artifact_path = incoming_dir / "claude-incident.md"
        artifact_path.write_text("# Claude Incident\n", encoding="utf-8")
        manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T00:00:00Z",
            "artifact_path": "incoming/claude-incident.md",
            "artifact_type": "incident_memo",
            "source_agent": "claude-work-agent",
            "requested_action": "ingest_and_update_case_state",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
        }
        (exchange_root / "manifests" / "20260307T000000Z-incident_memo.json").write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        intake_dir = self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "incident_memo"
        self.assertTrue(any(path.name.endswith("claude-incident.md") for path in intake_dir.iterdir()))
        tasks_text = (self.root / "shared" / "tasks.yaml").read_text(encoding="utf-8")
        self.assertIn("Review ingested incident memo from claude-work-agent", tasks_text)
        memory_text = (self.root / "knowledge" / "memory.jsonl").read_text(encoding="utf-8")
        self.assertIn('"type": "agent_exchange_ingest"', memory_text)
        self.assertFalse(artifact_path.exists())
        self.assertTrue(any(path.name.endswith("claude-incident.md") for path in (incoming_dir / "processed").iterdir()))
        self.assertTrue(any(path.name.endswith("incident_memo.json") for path in (exchange_root / "manifests" / "processed").iterdir()))

        structured_artifact = incoming_dir / "claude-decision.md"
        structured_artifact.write_text("# Decision\n", encoding="utf-8")
        structured_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T00:05:00Z",
            "artifact_path": "incoming/claude-decision.md",
            "artifact_type": "decision_memo",
            "source_agent": "claude-work-agent",
            "requested_action": "ingest_and_update_case_state",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "codex_state_patch": {
                "matter_status": {
                    "filing.filing_readiness": "ready_pending_lawyer",
                },
                "claim_updates": [
                    {
                        "id": "C1",
                        "set": {
                            "forum_track": "canada_or_cross_border",
                        },
                    }
                ],
            },
        }
        (exchange_root / "manifests" / "20260307T000500Z-decision_memo.json").write_text(
            json.dumps(structured_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        proposals_dir = self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals"
        proposals = list(proposals_dir.glob("*.json"))
        self.assertEqual(len(proposals), 1)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "agent-proposal-status"])
        self.assertEqual(code, 0)
        self.assertIn("[pending]", stdout.getvalue())

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-proposal-apply",
                    "--path",
                    str(proposals[0]),
                ]
            )
        self.assertEqual(code, 0)
        matter_status_text = (self.root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml").read_text(encoding="utf-8")
        self.assertIn("filing_readiness: ready_pending_lawyer", matter_status_text)
        claims_text = (self.root / "nrg-bloom" / "litigation-ton" / "claims-map.yaml").read_text(encoding="utf-8")
        self.assertIn("forum_track: canada_or_cross_border", claims_text)

        review_artifact = incoming_dir / "claude-review.md"
        review_artifact.write_text("# Review\n", encoding="utf-8")
        review_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T00:10:00Z",
            "artifact_path": "incoming/claude-review.md",
            "artifact_type": "decision_memo",
            "source_agent": "claude-work-agent",
            "requested_action": "ingest_and_update_case_state",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "codex_state_updates_suggested": {
                "strategy": "top_action should change",
            },
        }
        (exchange_root / "manifests" / "20260307T001000Z-review_decision_memo.json").write_text(
            json.dumps(review_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "agent-proposal-status"])
        self.assertEqual(code, 0)
        self.assertIn("[pending_review]", stdout.getvalue())
        self.assertIn("suggested_updates", stdout.getvalue())

        proposals = sorted((self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals").glob("*.json"))
        pending_review_path = next(
            path
            for path in proposals
            if "decision_memo" in path.name and '"status": "pending_review"' in path.read_text(encoding="utf-8")
        )
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(["--workspace", str(self.root), "agent-proposal-promote", "--path", str(pending_review_path)])
        self.assertEqual(code, 0)
        promoted_text = pending_review_path.read_text(encoding="utf-8")
        self.assertIn('"status": "pending"', promoted_text)
        self.assertIn('"patch"', promoted_text)

        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "agent-review-queue"])
        self.assertEqual(code, 0)
        review_output = stdout.getvalue()
        self.assertIn("agent review queue", review_output)
        self.assertIn("recent ingested artifacts", review_output)
        self.assertIn("proposal queue", review_output)
        self.assertIn("open review tasks", review_output)

        structured_apply_artifact = incoming_dir / "claude-apply.md"
        structured_apply_artifact.write_text(
            "# Apply\n\n```json\n"
            "{"
            "\"matter_status\": {"
            "\"canadian_path\": \"confirmed_pressure_filing\","
            "\"canadian_path_scope\": \"file_and_serve\","
            "\"canadian_path_budget_cap\": \"$5,000 CAD\","
            "\"filing_readiness\": \"ready_pending_lawyer\""
            "},"
            "\"claim_updates\": [{\"id\": \"C1\", \"set\": {\"forum_track\": \"alberta_primary\"}}],"
            "\"anti_stay_posture\": [\"keep MNDA claims in Alberta\"],"
            "\"strategy_principles_add\": [\"Alberta is a pressure device\"],"
            "\"leverage_points_add\": [{\"name\": \"Alberta protective filing\", \"deployed\": false, \"impact\": \"High\"}]"
            "}\n```\n",
            encoding="utf-8",
        )
        structured_apply_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T00:20:00Z",
            "artifact_path": "incoming/claude-apply.md",
            "artifact_type": "codex_response",
            "source_agent": "claude-work-agent",
            "requested_action": "apply_structured_patch",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
        }
        (exchange_root / "manifests" / "20260307T002000Z-codex_apply.json").write_text(
            json.dumps(structured_apply_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        proposals = sorted((self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals").glob("*.json"))
        apply_target = next(path for path in proposals if "codex_response" in path.name)
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(["--workspace", str(self.root), "agent-proposal-apply", "--path", str(apply_target)])
        self.assertEqual(code, 0)
        matter_status_text = (self.root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml").read_text(encoding="utf-8")
        self.assertIn("canadian_path: confirmed_pressure_filing", matter_status_text)
        self.assertIn("canadian_path_scope: file_and_serve", matter_status_text)
        self.assertIn("canadian_path_budget_cap: $5,000 CAD", matter_status_text)
        self.assertIn("anti_stay_posture", matter_status_text)
        self.assertIn("strategy_principles", matter_status_text)
        tracker_text = (self.root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml").read_text(encoding="utf-8")
        self.assertIn("Alberta protective filing", tracker_text)

        response_artifact = incoming_dir / "claude-response.md"
        response_artifact.write_text(
            "# Response\n\n```json\n{\"matter_status\": {\"filing.filing_readiness\": \"ready_pending_lawyer\"}}\n```\n",
            encoding="utf-8",
        )
        response_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T00:15:00Z",
            "artifact_path": "incoming/claude-response.md",
            "artifact_type": "codex_response",
            "source_agent": "claude-work-agent",
            "requested_action": "apply_structured_patch",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
        }
        (exchange_root / "manifests" / "20260307T001500Z-codex_response.json").write_text(
            json.dumps(response_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "agent-proposal-status"])
        self.assertEqual(code, 0)
        self.assertIn("[pending]", stdout.getvalue())

    def test_scheduler_run_command(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            exit_code = run(["--workspace", str(self.root), "scheduler-run", "--cycles", "1"])
        output = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("scheduler report generated", output)
        self.assertIn("Protective filing decision", output)
        heartbeat_path = self.root / ".work_codex" / "scheduler" / "last_run.json"
        self.assertTrue(heartbeat_path.exists())

    def test_agent_exchange_ingest_accepts_strategic_plan(self) -> None:
        exchange_root = self.root / "exchange"
        incoming_dir = exchange_root / "incoming"
        manifests_dir = exchange_root / "manifests"
        incoming_dir.mkdir(parents=True)
        manifests_dir.mkdir(parents=True)
        (manifests_dir / "manifest-template.json").write_text("{}", encoding="utf-8")

        plan_artifact = incoming_dir / "sentinel-plan.md"
        plan_artifact.write_text("# Strategic Plan\n\nTrack 1 and Track 2.", encoding="utf-8")
        plan_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T02:00:00Z",
            "artifact_path": "incoming/sentinel-plan.md",
            "artifact_type": "strategic_plan",
            "source_agent": "sentinel",
            "requested_action": "ingest_and_update_case_state",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "codex_state_updates_suggested": {
                "matter_status": {
                    "phase": "active_proceedings_preparation",
                }
            },
        }
        (manifests_dir / "20260307T020000Z-strategic_plan.json").write_text(
            json.dumps(plan_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn("ingested 1 artifact(s)", stdout.getvalue())

        intake_dir = self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "strategic_plan"
        ingested = sorted(intake_dir.glob("*.md"))
        self.assertEqual(len(ingested), 1)
        proposals = sorted((self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals").glob("*.json"))
        proposal_path = next(path for path in proposals if "strategic_plan" in path.name)
        self.assertTrue(proposal_path.exists())

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(["--workspace", str(self.root), "agent-proposal-promote", "--path", str(proposal_path)])
        self.assertEqual(code, 0)

        promoted = json.loads(proposal_path.read_text(encoding="utf-8"))
        self.assertEqual(promoted["status"], "pending")
        self.assertEqual(promoted["patch"]["matter_status"]["phase"], "active_proceedings_preparation")

    def test_agent_exchange_ingest_accepts_strategic_response_with_aegis_updates(self) -> None:
        exchange_root = self.root / "exchange"
        incoming_dir = exchange_root / "incoming"
        manifests_dir = exchange_root / "manifests"
        incoming_dir.mkdir(parents=True)
        manifests_dir.mkdir(parents=True)
        (manifests_dir / "manifest-template.json").write_text("{}", encoding="utf-8")

        response_artifact = incoming_dir / "sentinel-response.md"
        response_artifact.write_text("# Strategic Response\n", encoding="utf-8")
        response_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-08T16:00:00Z",
            "artifact_path": "incoming/sentinel-response.md",
            "artifact_type": "strategic_response",
            "source_agent": "sentinel",
            "requested_action": "ingest_and_update_live_notes",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "aegis_state_updates_suggested": {
                "content_use_policy": "ACTIVE",
                "live_notes_add": "Content is evidence first."
            },
        }
        (manifests_dir / "20260308T160000Z-strategic_response.json").write_text(
            json.dumps(response_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 8)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn("ingested 1 artifact(s)", stdout.getvalue())

        intake_dir = self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "strategic_response"
        ingested = sorted(intake_dir.glob("*.md"))
        self.assertEqual(len(ingested), 1)
        proposals = sorted((self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals").glob("*.json"))
        proposal_path = next(path for path in proposals if "strategic_response" in path.name)
        payload = json.loads(proposal_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "pending_review")
        self.assertIn("content_use_policy", payload["suggested_updates"])

    def test_agent_exchange_ingest_accepts_session_summary(self) -> None:
        exchange_root = self.root / "exchange"
        incoming_dir = exchange_root / "incoming"
        manifests_dir = exchange_root / "manifests"
        incoming_dir.mkdir(parents=True)
        manifests_dir.mkdir(parents=True)
        (manifests_dir / "manifest-template.json").write_text("{}", encoding="utf-8")

        summary_artifact = incoming_dir / "sentinel-session-update.md"
        summary_artifact.write_text("# Session Summary\n", encoding="utf-8")
        summary_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-09T18:00:00Z",
            "artifact_path": "incoming/sentinel-session-update.md",
            "artifact_type": "session_summary",
            "source_agent": "sentinel",
            "requested_action": "ingest_and_update_case_state",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "aegis_state_updates_suggested": {
                "matter_status": {"phase": "active_court_proceedings"},
                "live_notes_append": "Court proceedings beginning this week."
            },
        }
        (manifests_dir / "20260309T180000Z-session_summary.json").write_text(
            json.dumps(summary_manifest),
            encoding="utf-8",
        )

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 9)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn("ingested 1 artifact(s)", stdout.getvalue())

        intake_dir = self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "session_summary"
        ingested = sorted(intake_dir.glob("*.md"))
        self.assertEqual(len(ingested), 1)

    def test_agent_exchange_ingest_marks_superseded_plan(self) -> None:
        exchange_root = self.root / "exchange"
        incoming_dir = exchange_root / "incoming"
        manifests_dir = exchange_root / "manifests"
        incoming_dir.mkdir(parents=True)
        manifests_dir.mkdir(parents=True)
        (manifests_dir / "manifest-template.json").write_text("{}", encoding="utf-8")

        v1_artifact = incoming_dir / "sentinel-plan-v1.md"
        v1_artifact.write_text("# Strategic Plan V1\n", encoding="utf-8")
        v1_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T01:00:00Z",
            "artifact_path": "incoming/sentinel-plan-v1.md",
            "artifact_type": "strategic_plan",
            "source_agent": "sentinel",
            "requested_action": "ingest_and_update_case_state",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "codex_state_updates_suggested": {"matter_status": {"phase": "negotiation_window_plus_arbitration_prep"}},
        }
        (manifests_dir / "20260307T010000Z-strategic_plan_v1.json").write_text(json.dumps(v1_manifest), encoding="utf-8")

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)

        v2_artifact = incoming_dir / "sentinel-plan-v2.md"
        v2_artifact.write_text("# Strategic Plan V2\n", encoding="utf-8")
        v2_manifest = {
            "protocol_version": "agent-exchange-manifest/v1",
            "created_at_utc": "2026-03-07T02:00:00Z",
            "artifact_path": "incoming/sentinel-plan-v2.md",
            "artifact_type": "strategic_plan",
            "source_agent": "sentinel",
            "requested_action": "ingest_and_replace_v1",
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "supersedes": "incoming/sentinel-plan-v1.md",
            "codex_state_updates_suggested": {"matter_status": {"phase": "active_proceedings_preparation"}},
        }
        (manifests_dir / "20260307T020000Z-strategic_plan_v2.json").write_text(json.dumps(v2_manifest), encoding="utf-8")

        stdout = StringIO()
        with patch("sys.stdout", stdout), patch("work_codex.cli.date") as mocked_date:
            mocked_date.today.return_value = date(2026, 3, 7)
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "agent-exchange-ingest",
                    "--exchange-root",
                    str(exchange_root),
                ]
            )
        self.assertEqual(code, 0)

        replacement_dir = self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals"
        replacement = [path for path in sorted(replacement_dir.glob("*.json")) if "strategic_plan" in path.name][-1]
        supersede_matching_proposals(
            self.root,
            source_agent="sentinel",
            artifact_type="strategic_plan",
            supersedes="incoming/sentinel-plan-v1.md",
            replacement_proposal_path=replacement,
            today=date(2026, 3, 7),
        )

        proposals = sorted((self.root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals").glob("*.json"))
        payloads = [json.loads(path.read_text(encoding="utf-8")) for path in proposals if "strategic_plan" in path.name]
        self.assertTrue(any(item.get("status") == "superseded" for item in payloads))
        self.assertTrue(any(item.get("supersedes") == "incoming/sentinel-plan-v1.md" for item in payloads))

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
