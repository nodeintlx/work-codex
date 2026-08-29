from __future__ import annotations

from io import StringIO
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from work_codex.authority_engine import generate_authority_system, generate_weekly_authority_batch
from work_codex.cli import run


FACTS_YAML = """
facts:
  - id: "market_fact"
    claim: "A real external market signal exists."
    status: "verified"
    scope: "external"
    sources:
      - path: "report/a"
        type: "official_report"
        authority: "institutional"
        excerpt: "Source A"
      - path: "report/b"
        type: "regulator"
        authority: "institutional"
        excerpt: "Source B"
      - path: "report/c"
        type: "trusted_media"
        authority: "media"
        excerpt: "Source C"
  - id: "proof_fact"
    claim: "NRG Bloom has operating proof."
    status: "verified"
    scope: "internal"
    sources:
      - path: "docs/a.md"
        type: "internal_doc"
        authority: "internal"
        excerpt: "Source A"
      - path: "docs/b.md"
        type: "internal_doc"
        authority: "internal"
        excerpt: "Source B"
      - path: "docs/c.md"
        type: "internal_doc"
        authority: "internal"
        excerpt: "Source C"
"""


PLAN_YAML = """
slug: "authority-foundation"
title: "Authority Foundation"
fact_registry: "../../content-engine/facts/facts.yaml"
core_principle: "Stay visible through market authority."
inputs:
  - "Market signals"
constraints:
  - "No live-sensitive details"
intake_fields:
  - "source link"
source_watchlist:
  - name: "IEA"
    tier: "institutional_primary"
    type: "energy"
    url: "https://example.com/iea"
    why_it_matters: "Important market signal"
    tracking_focus: ["power demand"]
objections:
  - slug: "why_now"
    question: "Why now?"
    answer: "Timing is improving."
    formats: ["Founder post"]
    fact_ids: ["market_fact"]
franchises:
  - slug: "market-intelligence"
    name: "Market Intelligence"
    purpose: "Interpret the market"
    audiences: ["investors"]
    tone: "measured"
    formats: ["thread", "market note"]
    fact_ids: ["market_fact", "proof_fact"]
weekly_lanes:
  - day: "Monday"
    lane: "market-intelligence"
    objective: "Lead the week."
    output: "Founder post"
    objection: "Why now?"
    objection_slug: "why_now"
distribution_rules:
  - "Ship one fact-led piece."
founder_insight_rules:
  - "Keep it sanitized."
"""


class AuthorityEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "nrg-bloom" / "authority-engine" / "plans").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "facts").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "facts" / "facts.yaml").write_text(
            textwrap.dedent(FACTS_YAML).strip() + "\n",
            encoding="utf-8",
        )
        (self.root / "nrg-bloom" / "authority-engine" / "plans" / "plan.yaml").write_text(
            textwrap.dedent(PLAN_YAML).strip() + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_generate_authority_system(self) -> None:
        built = generate_authority_system(self.root, self.root / "nrg-bloom" / "authority-engine" / "plans" / "plan.yaml")
        self.assertTrue((built.output_dir / "authority-operating-system.md").exists())
        self.assertTrue((built.output_dir / "source-watchlist.yaml").exists())
        self.assertTrue((built.output_dir / "investor-objection-bank.yaml").exists())
        self.assertTrue((built.output_dir / "evergreen-franchise-map.yaml").exists())
        self.assertTrue((built.output_dir / "external-intel-queue.yaml").exists())
        text = (built.output_dir / "investor-objection-bank.md").read_text(encoding="utf-8")
        self.assertIn("Why now?", text)
        self.assertIn("A real external market signal exists.", text)

    def test_generate_weekly_authority_batch(self) -> None:
        built = generate_weekly_authority_batch(self.root, self.root / "nrg-bloom" / "authority-engine" / "plans" / "plan.yaml")
        self.assertTrue((built.output_dir / "weekly-authority-batch.md").exists())
        self.assertTrue((built.output_dir / "weekly-authority-queue.yaml").exists())
        self.assertTrue((built.output_dir / "editorial-prompt-pack.md").exists())

    def test_cli_authority_build(self) -> None:
        stdout = StringIO()
        plan_path = self.root / "nrg-bloom" / "authority-engine" / "plans" / "plan.yaml"
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "authority-os-build", "--plan", str(plan_path)])
        self.assertEqual(code, 0)
        self.assertIn("built authority system:", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
