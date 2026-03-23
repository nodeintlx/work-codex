"""Tests for BloomFlow v2 Phase 0 — database, state machine, function API, migration."""

from __future__ import annotations

import sqlite3
import tempfile
import textwrap
import unittest
from datetime import date
from pathlib import Path

from work_codex.bloomflow import (
    Brief,
    BriefStatus,
    InvalidTransition,
    QueueItem,
    QueueStatus,
    add_queue_item,
    create_brief,
    get_brief,
    get_queue_item,
    list_briefs,
    list_queue,
    migrate_from_yaml,
    transition_brief,
    transition_queue_item,
    update_brief,
)
from work_codex.bloomflow.db import init_db, open_db
from work_codex.bloomflow.states import (
    queue_status_for_brief,
    validate_brief_transition,
    validate_queue_transition,
)


class TestStateMachine(unittest.TestCase):
    """Test explicit state transitions."""

    # --- Brief transitions ---

    def test_brief_drafting_ready_to_approved_for_drafting(self):
        validate_brief_transition(BriefStatus.DRAFTING_READY, BriefStatus.APPROVED_FOR_DRAFTING)

    def test_brief_drafting_ready_to_paused(self):
        validate_brief_transition(BriefStatus.DRAFTING_READY, BriefStatus.PAUSED)

    def test_brief_drafting_ready_to_published_blocked(self):
        with self.assertRaises(InvalidTransition):
            validate_brief_transition(BriefStatus.DRAFTING_READY, BriefStatus.PUBLISHED)

    def test_brief_in_review_to_approved(self):
        validate_brief_transition(BriefStatus.IN_REVIEW, BriefStatus.APPROVED)

    def test_brief_in_review_to_drafting_ready(self):
        validate_brief_transition(BriefStatus.IN_REVIEW, BriefStatus.DRAFTING_READY)

    def test_brief_approved_to_scheduled(self):
        validate_brief_transition(BriefStatus.APPROVED, BriefStatus.SCHEDULED)

    def test_brief_scheduled_to_published(self):
        validate_brief_transition(BriefStatus.SCHEDULED, BriefStatus.PUBLISHED)

    def test_brief_published_is_terminal(self):
        with self.assertRaises(InvalidTransition):
            validate_brief_transition(BriefStatus.PUBLISHED, BriefStatus.PAUSED)

    def test_brief_paused_to_drafting_ready(self):
        validate_brief_transition(BriefStatus.PAUSED, BriefStatus.DRAFTING_READY)

    def test_brief_paused_to_scheduled_blocked(self):
        with self.assertRaises(InvalidTransition):
            validate_brief_transition(BriefStatus.PAUSED, BriefStatus.SCHEDULED)

    # --- Queue transitions ---

    def test_queue_backlog_to_planned(self):
        validate_queue_transition(QueueStatus.BACKLOG, QueueStatus.PLANNED)

    def test_queue_backlog_to_published_blocked(self):
        with self.assertRaises(InvalidTransition):
            validate_queue_transition(QueueStatus.BACKLOG, QueueStatus.PUBLISHED)

    def test_queue_published_is_terminal(self):
        with self.assertRaises(InvalidTransition):
            validate_queue_transition(QueueStatus.PUBLISHED, QueueStatus.BACKLOG)

    def test_queue_paused_to_backlog(self):
        validate_queue_transition(QueueStatus.PAUSED, QueueStatus.BACKLOG)

    # --- Sync mapping ---

    def test_queue_status_for_brief_drafting_ready(self):
        self.assertEqual(queue_status_for_brief(BriefStatus.DRAFTING_READY), QueueStatus.BACKLOG)

    def test_queue_status_for_brief_published(self):
        self.assertEqual(queue_status_for_brief(BriefStatus.PUBLISHED), QueueStatus.PUBLISHED)


class TestDatabase(unittest.TestCase):
    """Test database setup and schema."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test.db"
        self.conn = open_db(self.db_path)
        init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_schema_version(self):
        row = self.conn.execute("SELECT version FROM schema_version").fetchone()
        self.assertEqual(row["version"], 1)

    def test_tables_exist(self):
        tables = {
            row[0]
            for row in self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        self.assertIn("briefs", tables)
        self.assertIn("queue_items", tables)
        self.assertIn("audit_log", tables)

    def test_init_db_idempotent(self):
        init_db(self.conn)
        init_db(self.conn)
        row = self.conn.execute("SELECT COUNT(*) AS n FROM schema_version").fetchone()
        self.assertEqual(row["n"], 1)


class TestBriefAPI(unittest.TestCase):
    """Test brief CRUD and transitions."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test.db"
        self.conn = open_db(self.db_path)
        init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_create_and_get_brief(self):
        brief = create_brief(
            self.conn,
            title="Test brief",
            raw_idea="This is a test idea.",
            today=date(2026, 3, 10),
            audience_primary="founders",
            content_pillar="builder_credibility",
            funnel_stage="awareness",
        )
        self.assertIsInstance(brief, Brief)
        self.assertEqual(brief.title, "Test brief")
        self.assertEqual(brief.status, "drafting_ready")
        self.assertEqual(brief.audience_primary, "founders")
        self.assertEqual(brief.created_at, "2026-03-10")

        fetched = get_brief(self.conn, brief.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, brief.id)

    def test_create_brief_auto_id(self):
        b1 = create_brief(self.conn, title="First", raw_idea="idea 1")
        b2 = create_brief(self.conn, title="Second", raw_idea="idea 2")
        self.assertEqual(b1.id, "CB-001")
        self.assertEqual(b2.id, "CB-002")

    def test_list_briefs(self):
        create_brief(self.conn, title="A", raw_idea="a")
        create_brief(self.conn, title="B", raw_idea="b")
        self.assertEqual(len(list_briefs(self.conn)), 2)

    def test_list_briefs_by_status(self):
        create_brief(self.conn, title="A", raw_idea="a", status="drafting_ready")
        create_brief(self.conn, title="B", raw_idea="b", status="in_review")
        self.assertEqual(len(list_briefs(self.conn, status="drafting_ready")), 1)
        self.assertEqual(len(list_briefs(self.conn, status="in_review")), 1)

    def test_update_brief(self):
        brief = create_brief(self.conn, title="Original", raw_idea="idea")
        updated = update_brief(self.conn, brief.id, title="Revised", main_thesis="new thesis")
        self.assertEqual(updated.title, "Revised")
        self.assertEqual(updated.main_thesis, "new thesis")
        self.assertEqual(updated.status, "drafting_ready")  # unchanged

    def test_update_brief_ignores_status(self):
        brief = create_brief(self.conn, title="T", raw_idea="i")
        updated = update_brief(self.conn, brief.id, status="published", title="T2")
        self.assertEqual(updated.status, "drafting_ready")  # status change blocked

    def test_update_brief_not_found(self):
        with self.assertRaises(ValueError):
            update_brief(self.conn, "CB-999", title="X")

    def test_transition_brief(self):
        brief = create_brief(self.conn, title="T", raw_idea="i")
        moved = transition_brief(self.conn, brief.id, "approved_for_drafting")
        self.assertEqual(moved.status, "approved_for_drafting")

    def test_transition_brief_invalid(self):
        brief = create_brief(self.conn, title="T", raw_idea="i")
        with self.assertRaises(InvalidTransition):
            transition_brief(self.conn, brief.id, "published")

    def test_transition_brief_not_found(self):
        with self.assertRaises(ValueError):
            transition_brief(self.conn, "CB-999", "in_review")

    def test_transition_brief_full_lifecycle(self):
        brief = create_brief(self.conn, title="T", raw_idea="i")
        self.assertEqual(brief.status, "drafting_ready")

        brief = transition_brief(self.conn, brief.id, "approved_for_drafting")
        self.assertEqual(brief.status, "approved_for_drafting")

        brief = transition_brief(self.conn, brief.id, "in_review")
        self.assertEqual(brief.status, "in_review")

        brief = transition_brief(self.conn, brief.id, "approved")
        self.assertEqual(brief.status, "approved")

        brief = transition_brief(self.conn, brief.id, "scheduled", scheduled_for="2026-04-01")
        self.assertEqual(brief.status, "scheduled")
        self.assertEqual(brief.publish_window, "2026-04-01")

        brief = transition_brief(self.conn, brief.id, "published", published_at="2026-04-01")
        self.assertEqual(brief.status, "published")
        self.assertTrue(brief.performance.get("published_assets"))

    def test_transition_brief_syncs_queue(self):
        qi = add_queue_item(self.conn, title="T", id="CM-001", brief_id="CB-001")
        brief = create_brief(self.conn, title="T", raw_idea="i", source_ref="CM-001")
        transition_brief(self.conn, brief.id, "approved_for_drafting")
        qi = get_queue_item(self.conn, "CM-001")
        self.assertEqual(qi.status, "backlog")  # approved_for_drafting maps to backlog

        transition_brief(self.conn, brief.id, "in_review")
        qi = get_queue_item(self.conn, "CM-001")
        self.assertEqual(qi.status, "in_review")

    def test_json_fields_roundtrip(self):
        hooks = ["hook 1", "hook 2", "hook 3"]
        creative = {"visual_theme": "sharp", "thumbnail_concepts": ["bold text"]}
        brief = create_brief(
            self.conn,
            title="JSON test",
            raw_idea="test",
            hooks=hooks,
            creative_direction=creative,
        )
        fetched = get_brief(self.conn, brief.id)
        self.assertEqual(fetched.hooks, hooks)
        self.assertEqual(fetched.creative_direction, creative)

    def test_get_brief_not_found(self):
        self.assertIsNone(get_brief(self.conn, "CB-999"))

    def test_invalid_status_on_create(self):
        with self.assertRaises(ValueError):
            create_brief(self.conn, title="T", raw_idea="i", status="nonexistent")


class TestQueueAPI(unittest.TestCase):
    """Test queue item CRUD and transitions."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test.db"
        self.conn = open_db(self.db_path)
        init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_add_and_get_queue_item(self):
        item = add_queue_item(
            self.conn,
            title="Post about execution",
            pillar="builder_credibility",
            audience="founders",
        )
        self.assertIsInstance(item, QueueItem)
        self.assertEqual(item.title, "Post about execution")
        self.assertEqual(item.status, "backlog")

        fetched = get_queue_item(self.conn, item.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, item.id)

    def test_auto_id(self):
        q1 = add_queue_item(self.conn, title="A")
        q2 = add_queue_item(self.conn, title="B")
        self.assertEqual(q1.id, "CM-001")
        self.assertEqual(q2.id, "CM-002")

    def test_list_queue(self):
        add_queue_item(self.conn, title="A")
        add_queue_item(self.conn, title="B")
        self.assertEqual(len(list_queue(self.conn)), 2)

    def test_list_queue_by_status(self):
        add_queue_item(self.conn, title="A", status="backlog")
        add_queue_item(self.conn, title="B", status="planned")
        self.assertEqual(len(list_queue(self.conn, status="backlog")), 1)

    def test_transition_queue_item(self):
        item = add_queue_item(self.conn, title="T")
        moved = transition_queue_item(self.conn, item.id, "planned")
        self.assertEqual(moved.status, "planned")

    def test_transition_queue_item_invalid(self):
        item = add_queue_item(self.conn, title="T")
        with self.assertRaises(InvalidTransition):
            transition_queue_item(self.conn, item.id, "published")

    def test_transition_queue_item_not_found(self):
        with self.assertRaises(ValueError):
            transition_queue_item(self.conn, "CM-999", "planned")

    def test_repurpose_channels_roundtrip(self):
        channels = ["x", "email"]
        item = add_queue_item(self.conn, title="T", repurpose_channels=channels)
        fetched = get_queue_item(self.conn, item.id)
        self.assertEqual(fetched.repurpose_channels, channels)

    def test_get_queue_item_not_found(self):
        self.assertIsNone(get_queue_item(self.conn, "CM-999"))


class TestMigration(unittest.TestCase):
    """Test YAML to SQLite migration."""

    def _make_workspace(self, tmp: str) -> Path:
        root = Path(tmp)
        briefs_dir = root / "nrg-bloom" / "marketing" / "briefs"
        briefs_dir.mkdir(parents=True)

        brief_yaml = textwrap.dedent("""\
            id: CB-001
            created_at: '2026-03-10'
            updated_at: '2026-03-10'
            status: in_review
            owner: makir
            source_type: content_intake
            source_ref: CM-008
            title: How founder optimism breaks execution
            raw_idea: Founders think momentum is enough.
            audience:
              primary: founders
              secondary:
                - x
            content_pillar: founder_lessons
            funnel_stage: awareness
            main_thesis: Real thesis here.
            punch_idea: Sharp takeaway.
            hooks:
              - hook 1
              - hook 2
              - hook 3
            primary_format: linkedin_post
            primary_channel: linkedin
            primary_cta: Follow NRG Bloom.
            guardrails:
              legal_risk_level: safe_public_generic
            creative_direction:
              visual_theme: sharp editorial
            drafts:
              linkedin: ''
              x_thread: ''
            performance:
              published_assets: []
        """)
        (briefs_dir / "cb-001-test.yaml").write_text(brief_yaml, encoding="utf-8")

        queue_yaml = textwrap.dedent("""\
            last_updated: '2026-03-10'
            cadence:
              weekly_posts: 3
              publish_days:
                - Tuesday
                - Thursday
            items:
              - id: CM-001
                status: planned
                scheduled_for: '2026-03-12'
                title: What a year taught me
                pillar: builder_credibility
                audience: founders
                funnel_stage: awareness
                primary_channel: linkedin
                repurpose_channels:
                  - x
                  - email
                cta: Follow NRG Bloom.
                lead_magnet: Field Notes memo
                source: phase_1_seed
              - id: CM-008
                brief_id: CB-001
                status: in_review
                title: How founder optimism breaks execution
                pillar: founder_lessons
                audience: founders
                funnel_stage: awareness
                primary_channel: linkedin
                repurpose_channels:
                  - x
                  - email
                cta: Follow NRG Bloom.
                lead_magnet: Field Notes memo
                suggested_publish_date: '2026-03-26'
                source: content-intake
        """)
        (root / "nrg-bloom" / "marketing" / "content-queue.yaml").write_text(
            queue_yaml, encoding="utf-8"
        )
        return root

    def test_migrate_from_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_workspace(tmp)
            db_path = Path(tmp) / "test.db"
            result = migrate_from_yaml(root, db_path=db_path)

            self.assertTrue(result.ok)
            self.assertEqual(result.briefs_migrated, 1)
            self.assertEqual(result.queue_items_migrated, 2)

            conn = open_db(db_path)
            try:
                brief = get_brief(conn, "CB-001")
                self.assertIsNotNone(brief)
                self.assertEqual(brief.title, "How founder optimism breaks execution")
                self.assertEqual(brief.status, "in_review")
                self.assertEqual(brief.audience_primary, "founders")
                self.assertEqual(brief.hooks, ["hook 1", "hook 2", "hook 3"])

                qi = get_queue_item(conn, "CM-001")
                self.assertIsNotNone(qi)
                self.assertEqual(qi.title, "What a year taught me")
                self.assertEqual(qi.status, "planned")
                self.assertEqual(qi.repurpose_channels, ["x", "email"])

                qi2 = get_queue_item(conn, "CM-008")
                self.assertIsNotNone(qi2)
                self.assertEqual(qi2.brief_id, "CB-001")
            finally:
                conn.close()

    def test_migrate_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_workspace(tmp)
            db_path = Path(tmp) / "test.db"
            r1 = migrate_from_yaml(root, db_path=db_path)
            r2 = migrate_from_yaml(root, db_path=db_path)

            self.assertEqual(r1.briefs_migrated, 1)
            self.assertEqual(r2.briefs_migrated, 0)
            self.assertEqual(r2.briefs_skipped, 1)
            self.assertEqual(r1.queue_items_migrated, 2)
            self.assertEqual(r2.queue_items_migrated, 0)
            self.assertEqual(r2.queue_items_skipped, 2)

    def test_migrate_missing_briefs_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "nrg-bloom" / "marketing").mkdir(parents=True)
            queue_yaml = "last_updated: '2026-03-10'\nitems: []\n"
            (root / "nrg-bloom" / "marketing" / "content-queue.yaml").write_text(
                queue_yaml, encoding="utf-8"
            )
            db_path = Path(tmp) / "test.db"
            result = migrate_from_yaml(root, db_path=db_path)
            self.assertTrue(result.ok)
            self.assertEqual(result.briefs_migrated, 0)
            self.assertEqual(result.queue_items_migrated, 0)


class TestAuditLog(unittest.TestCase):
    """Test that operations write audit entries."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = open_db(Path(self.tmp.name) / "test.db")
        init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_create_brief_audited(self):
        create_brief(self.conn, title="T", raw_idea="i")
        row = self.conn.execute("SELECT * FROM audit_log WHERE action='brief_created'").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["entity_type"], "brief")

    def test_transition_brief_audited(self):
        brief = create_brief(self.conn, title="T", raw_idea="i")
        transition_brief(self.conn, brief.id, "approved_for_drafting")
        row = self.conn.execute("SELECT * FROM audit_log WHERE action='brief_transitioned'").fetchone()
        self.assertIsNotNone(row)

    def test_add_queue_item_audited(self):
        add_queue_item(self.conn, title="T")
        row = self.conn.execute("SELECT * FROM audit_log WHERE action='queue_item_added'").fetchone()
        self.assertIsNotNone(row)


if __name__ == "__main__":
    unittest.main()
