from __future__ import annotations

from io import StringIO
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from work_codex.cli import run
from work_codex.content_engine import generate_content_campaign


BRAND_YAML = """
name: "NRG Bloom"
tagline: "Remote compute infrastructure on stranded energy"
social_handle: "@NRGBloom"
colors:
  bg: "#0A0E1A"
  surface: "#111827"
  border: "#1F2937"
  accent: "#00C896"
  accent_warm: "#F59E0B"
  text: "#F9FAFB"
  text_muted: "#9CA3AF"
  text_dim: "#6B7280"
fonts:
  display: "Space Grotesk"
  body: "Inter"
voice: {}
design: {}
"""

CAMPAIGN_YAML = """
slug: "authority-sprint"
title: "NRG Bloom Authority Sprint"
brand: "../brand/brand-system.yaml"
fact_registry: "../facts/verified-facts.yaml"
positioning: "Operator truth over generic commentary."
editorial_thesis: "Codex batch."
briefs:
  - slug: "remote-ops-moat"
    title: "Remote Ops Moat"
    publish_day: "Monday"
    archetype: "remote-ops-notebook"
    pillar: "remote-operations"
    target_channel: "linkedin-founder"
    audience: ["investors"]
    hero_stat: "13 months in field conditions beats slideware."
    hook: "The moat is operational discipline."
    thesis: "Remote infrastructure is won operationally."
    proof_points:
      - "Coordination beats cosmetics."
      - "Recovery matters."
      - "Speed compounds."
    contrarian_take: "Operators beat architects."
    call_to_action: "We are building that category."
    discussion_question: "Would you underwrite proof or polish?"
    quote: "Uptime is a coordination problem."
    video_hook: "The moat is ops."
    video_close: "Proof beats posture."
    hashtags: ["#NRGBloom", "#Infrastructure"]
    fact_ids: ["field_proof"]
"""

FACTS_YAML = """
facts:
  - id: "field_proof"
    claim: "NRG Bloom has field proof."
    status: "verified"
    sources:
      - path: "docs/a.md"
        excerpt: "Source A"
      - path: "docs/b.md"
        excerpt: "Source B"
      - path: "docs/c.md"
        excerpt: "Source C"
"""


class ContentEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "nrg-bloom" / "content-engine" / "brand").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "campaigns").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "facts").mkdir(parents=True)
        (self.root / "nrg-bloom" / "content-engine" / "brand" / "brand-system.yaml").write_text(
            textwrap.dedent(BRAND_YAML).strip() + "\n",
            encoding="utf-8",
        )
        (self.root / "nrg-bloom" / "content-engine" / "facts" / "verified-facts.yaml").write_text(
            textwrap.dedent(FACTS_YAML).strip() + "\n",
            encoding="utf-8",
        )
        (self.root / "nrg-bloom" / "content-engine" / "campaigns" / "authority.yaml").write_text(
            textwrap.dedent(CAMPAIGN_YAML).strip() + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_generate_content_campaign(self) -> None:
        campaign_path = self.root / "nrg-bloom" / "content-engine" / "campaigns" / "authority.yaml"
        generated = generate_content_campaign(self.root, campaign_path)
        self.assertTrue(generated.output_dir.exists())
        self.assertTrue((generated.output_dir / "campaign-overview.md").exists())
        self.assertTrue((generated.output_dir / "quote-cards.html").exists())
        self.assertTrue((generated.output_dir / "factcheck-report.md").exists())
        brief_dir = generated.output_dir / "remote-ops-moat"
        self.assertTrue((brief_dir / "linkedin-founder.md").exists())
        self.assertTrue((brief_dir / "social-card.html").exists())
        self.assertTrue((brief_dir / "quote-card-portrait.html").exists())
        self.assertTrue((brief_dir / "quote-card-portrait.png").exists())
        self.assertTrue((brief_dir / "data-sheet.md").exists())
        self.assertTrue((brief_dir / "verification.json").exists())
        founder_text = (brief_dir / "linkedin-founder.md").read_text(encoding="utf-8")
        quote_card_text = (brief_dir / "quote-card-portrait.html").read_text(encoding="utf-8")
        data_sheet_text = (brief_dir / "data-sheet.md").read_text(encoding="utf-8")
        self.assertIn("Remote Ops Moat", founder_text)
        self.assertIn("The moat is operational discipline.", founder_text)
        self.assertIn("@NRGBloom", quote_card_text)
        self.assertIn("Verified Facts", data_sheet_text)

    def test_cli_content_campaign_generate(self) -> None:
        stdout = StringIO()
        campaign_path = self.root / "nrg-bloom" / "content-engine" / "campaigns" / "authority.yaml"
        with patch("sys.stdout", stdout):
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-campaign-generate",
                    "--campaign",
                    str(campaign_path),
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn("generated content campaign:", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
