from __future__ import annotations

from io import StringIO
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from work_codex.cli import run
from work_codex.factcheck import factcheck_campaign, load_fact_registry, write_factcheck_report


FACTS_YAML = """
facts:
  - id: "field_proof"
    claim: "NRG Bloom has field proof."
    status: "verified"
    scope: "hybrid"
    sources:
      - path: "docs/a.md"
        type: "internal_doc"
        authority: "internal"
        excerpt: "Source A"
      - path: "docs/b.md"
        type: "official_report"
        authority: "institutional"
        url: "https://example.com/b"
        excerpt: "Source B"
      - path: "docs/c.md"
        type: "trusted_media"
        authority: "media"
        excerpt: "Source C"
"""

CAMPAIGN_YAML = """
slug: "verified-campaign"
fact_registry: "../facts/verified-facts.yaml"
briefs:
  - slug: "proof"
    title: "Proof"
    fact_ids: ["field_proof"]
"""


class FactcheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "nrg-bloom" / "content-engine" / "campaigns").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "facts").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "facts" / "verified-facts.yaml").write_text(
            textwrap.dedent(FACTS_YAML).strip() + "\n",
            encoding="utf-8",
        )
        (self.root / "nrg-bloom" / "content-engine" / "campaigns" / "verified.yaml").write_text(
            textwrap.dedent(CAMPAIGN_YAML).strip() + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_load_fact_registry_requires_three_sources(self) -> None:
        registry = load_fact_registry(self.root / "nrg-bloom" / "content-engine" / "facts" / "verified-facts.yaml")
        self.assertIn("field_proof", registry)
        self.assertEqual(len(registry["field_proof"].sources), 3)
        self.assertEqual(registry["field_proof"].scope, "hybrid")
        self.assertEqual(registry["field_proof"].sources[1].url, "https://example.com/b")

    def test_factcheck_campaign_and_report(self) -> None:
        campaign_path = self.root / "nrg-bloom" / "content-engine" / "campaigns" / "verified.yaml"
        result = factcheck_campaign(self.root, campaign_path)
        output_dir = self.root / "factcheck-output"
        write_factcheck_report(output_dir, result)
        verification_path = output_dir / "proof" / "verification.json"
        self.assertTrue(verification_path.exists())
        self.assertIn("field_proof", verification_path.read_text(encoding="utf-8"))

    def test_cli_content_factcheck_run(self) -> None:
        stdout = StringIO()
        campaign_path = self.root / "nrg-bloom" / "content-engine" / "campaigns" / "verified.yaml"
        with patch("sys.stdout", stdout):
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-factcheck-run",
                    "--campaign",
                    str(campaign_path),
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn("wrote factcheck report:", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
