from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import health_check


class HealthCheckTests(unittest.TestCase):
    def test_repository_validates_itself(self):
        summary = health_check.build(health_check.ROOT)
        self.assertEqual(summary["structural_status"], "pass", summary["checks"])

    def test_post_requires_translation_symmetry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            posts = root / "_posts"
            posts.mkdir()
            fm = """---
layout: article
title: Test
date: 2026-01-01 00:00:00 +0000
lang: en
categories: [architecture]
description: Test
translations:
  - lang: en
    url: /architecture/2026/01/01/en-test/
---
<p class=\"note\">safe</p>
"""
            (posts / "2026-01-01-en-test.md").write_text(fm, encoding="utf-8")
            self.assertEqual(health_check.post_contracts(root)["status"], "fail")

    def test_redirect_cannot_duplicate_article_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            redirects = root / "posts"
            redirects.mkdir()
            (redirects / "old.html").write_text("---\nlayout: redirect\nredirect_to: /new/\n---\narticle body\n", encoding="utf-8")
            self.assertEqual(health_check.redirect_contracts(root)["status"], "fail")

    def test_provider_specific_control_surface_is_forbidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / ".github"
            path.mkdir()
            (path / "copilot-instructions.md").write_text("duplicate", encoding="utf-8")
            self.assertEqual(health_check.forbidden_surfaces(root)["status"], "fail")

    def test_repo_map_requires_existing_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ai").mkdir()
            (root / "ai/repo-map.json").write_text(json.dumps({"schema_version": "1.0", "routing": {"article": ["_posts/"]}}), encoding="utf-8")
            self.assertEqual(health_check.repo_map(root)["status"], "fail")


if __name__ == "__main__":
    unittest.main()
