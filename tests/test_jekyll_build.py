"""Cheap checks of tools/jekyll_build.sh that need no Docker: it parses, passes shellcheck and mounts read-only."""
from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "jekyll_build.sh"


class JekyllBuildTests(unittest.TestCase):
    def test_script_parses(self):
        result = subprocess.run(["sh", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which("shellcheck"), "shellcheck not installed")
    def test_script_passes_shellcheck(self):
        result = subprocess.run(["shellcheck", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_source_is_mounted_read_only_and_never_deployed(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('-v "$root":/src:ro', text)
        self.assertIn("test -f /src/_config.yml", text)
        self.assertNotIn("git push", text)


if __name__ == "__main__":
    unittest.main()
