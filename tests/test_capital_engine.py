from __future__ import annotations

from io import StringIO
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from work_codex.capital_engine import generate_capital_stack, generate_weekly_capital_batch
from work_codex.cli import run


FACTS_YAML = """
facts:
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
  - id: "market_fact"
    claim: "A large external market exists."
    status: "verified"
    scope: "external"
    sources:
      - path: "report/a"
        type: "official_report"
        authority: "institutional"
        excerpt: "Source A"
        url: "https://example.com/a"
      - path: "report/b"
        type: "regulator"
        authority: "institutional"
        excerpt: "Source B"
        url: "https://example.com/b"
      - path: "report/c"
        type: "trusted_media"
        authority: "media"
        excerpt: "Source C"
        url: "https://example.com/c"
"""


PLAN_YAML = """
slug: "capital-foundation"
title: "Capital Foundation"
fact_registry: "../facts/facts.yaml"
positioning: "Proof-led infrastructure company."
company:
  name: "NRG Bloom"
  headquarters: "Montreal"
  operating_geography: "Nigeria"
  operating_model: "Modular compute on stranded energy"
  current_stage: "Operating"
capital:
  core_thesis: "Invest behind proof."
  why_now: "Timing is improving."
  winning_hypothesis: "Execution matters."
  investor_fit: "Investors who understand infrastructure."
  raise_status: "Preparing."
  weekly_goal: "Create quality investor touches."
  use_of_funds:
    - "Scale deployments."
  next_step: "Book a diligence call."
evidence:
  company_proof: ["proof_fact"]
  market_timing: ["market_fact"]
  category_lineage: ["market_fact"]
audiences:
  - slug: "funds"
    name: "Funds"
    role_in_funnel: "Primary capital"
    thesis: "Back proof."
    conversion_goal: "Memo review"
    channels: ["LinkedIn"]
    cta: "Read memo"
    proof_fact_ids: ["proof_fact", "market_fact"]
objections:
  - question: "Is it real?"
    answer: "Yes."
    fact_ids: ["proof_fact"]
franchises:
  - slug: "operator-proof"
    name: "Operator Proof"
    investor_problem: "Is it real?"
    asset_types: ["Founder post"]
    conversion_target: "Diligence"
    fact_ids: ["proof_fact"]
weekly_sequence:
  - day: "Monday"
    asset_type: "Founder post"
    audience: "Funds"
    objective: "Lead with proof."
    theme: "Proof"
    franchise: "operator-proof"
public_site_sources:
  - title: "Example"
    url: "https://example.com"
"""


class CapitalEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "nrg-bloom" / "capital-engine" / "facts").mkdir(parents=True)
        (self.root / "nrg-bloom" / "capital-engine" / "plans").mkdir(parents=True)
        (self.root / "nrg-bloom" / "capital-engine" / "facts" / "facts.yaml").write_text(
            textwrap.dedent(FACTS_YAML).strip() + "\n",
            encoding="utf-8",
        )
        (self.root / "nrg-bloom" / "capital-engine" / "plans" / "plan.yaml").write_text(
            textwrap.dedent(PLAN_YAML).strip() + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_generate_capital_stack(self) -> None:
        built = generate_capital_stack(self.root, self.root / "nrg-bloom" / "capital-engine" / "plans" / "plan.yaml")
        self.assertTrue((built.output_dir / "investor-thesis" / "investor-memo.md").exists())
        self.assertTrue((built.output_dir / "diligence-room" / "proof-of-execution.md").exists())
        self.assertTrue((built.output_dir / "audience-map.yaml").exists())
        self.assertTrue((built.output_dir / "content-backlog.yaml").exists())
        self.assertTrue((built.output_dir / "capital-dashboard.html").exists())
        memo_text = (built.output_dir / "investor-thesis" / "investor-memo.md").read_text(encoding="utf-8")
        self.assertIn("Proof-led infrastructure company.", memo_text)
        self.assertIn("NRG Bloom has operating proof.", memo_text)

    def test_generate_weekly_batch(self) -> None:
        built = generate_weekly_capital_batch(self.root, self.root / "nrg-bloom" / "capital-engine" / "plans" / "plan.yaml")
        self.assertTrue((built.output_dir / "weekly-batch.md").exists())
        self.assertTrue((built.output_dir / "weekly-content-queue.yaml").exists())
        self.assertTrue((built.output_dir / "investor-touch-list.md").exists())

    def test_cli_capital_infra_build(self) -> None:
        stdout = StringIO()
        plan_path = self.root / "nrg-bloom" / "capital-engine" / "plans" / "plan.yaml"
        with patch("sys.stdout", stdout):
            code = run(["--workspace", str(self.root), "capital-infra-build", "--plan", str(plan_path)])
        self.assertEqual(code, 0)
        self.assertIn("built capital infrastructure:", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
