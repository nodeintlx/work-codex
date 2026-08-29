from __future__ import annotations

from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from work_codex.cli import run
from work_codex.motion_pack import build_motion_pack


class MotionPackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source_dir = self.root / "nrg-bloom" / "content-engine" / "generated" / "20260326T000000Z-authority-sprint"
        brief_dir = self.source_dir / "remote-ops-moat"
        brief_dir.mkdir(parents=True, exist_ok=True)
        latest_dir = self.root / "nrg-bloom" / "content-engine" / "generated" / "latest"
        latest_dir.mkdir(parents=True, exist_ok=True)
        (latest_dir / "LATEST.txt").write_text(str(self.source_dir) + "\n", encoding="utf-8")

        scene_spec = {
            "title": "Remote Ops Moat",
            "scenes": [
                {"text": "Remote ops is the moat", "highlight": "moat"},
                {"text": "Discipline beats slideware", "highlight": "Discipline"},
            ],
        }
        (brief_dir / "video-scenes.json").write_text(json.dumps(scene_spec) + "\n", encoding="utf-8")
        verification = {
            "slug": "remote-ops-moat",
            "title": "Remote Ops Moat",
            "fact_ids": ["field_proof"],
            "verified": True,
            "verification_standard": "3 local sources minimum per fact",
            "facts": [
                {
                    "id": "field_proof",
                    "claim": "NRG Bloom has field proof.",
                    "status": "verified",
                    "sources": [
                        {"path": "docs/a.md", "excerpt": "Source A"},
                        {"path": "docs/b.md", "excerpt": "Source B"},
                        {"path": "docs/c.md", "excerpt": "Source C"},
                    ],
                }
            ],
        }
        (brief_dir / "verification.json").write_text(json.dumps(verification) + "\n", encoding="utf-8")
        manifest = {
            "brand": {
                "name": "NRG Bloom",
                "tagline": "Remote compute infrastructure on stranded energy",
                "colors": {
                    "bg": "#0A0E1A",
                    "surface": "#111827",
                    "accent": "#00C896",
                    "text": "#F9FAFB",
                    "text_muted": "#9CA3AF",
                },
                "fonts": {
                    "display": "Space Grotesk",
                    "body": "Inter",
                },
            },
            "briefs": [
                {
                    "slug": "remote-ops-moat",
                    "title": "Remote Ops Moat",
                    "output_dir": str(brief_dir),
                }
            ],
        }
        (self.source_dir / "manifest.json").write_text(json.dumps(manifest) + "\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_motion_pack(self) -> None:
        built = build_motion_pack(self.root, self.source_dir)
        self.assertTrue((built.output_dir / "index.html").exists())
        self.assertTrue((built.output_dir / "remote-ops-moat-vertical.html").exists())
        self.assertTrue((built.output_dir / "remote-ops-moat-vertical.png").exists())
        self.assertTrue((built.output_dir / "remote-ops-moat-vertical.gif").exists())
        self.assertTrue((built.output_dir / "remote-ops-moat-proof.png").exists())
        html_text = (built.output_dir / "remote-ops-moat-vertical.html").read_text(encoding="utf-8")
        self.assertIn("Remote ops is the moat", html_text)
        self.assertIn("#00C896", html_text)

    def test_cli_content_motion_build(self) -> None:
        stdout = StringIO()
        with patch("sys.stdout", stdout):
            code = run(
                [
                    "--workspace",
                    str(self.root),
                    "content-motion-build",
                    "--source",
                    str(self.source_dir),
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn("built motion pack:", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
