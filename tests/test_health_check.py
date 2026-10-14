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


def article(lang: str, day: str = "2026-01-01", category: str = "architecture", **overrides: str) -> str:
    fields = {"layout": "article", "title": "Test", "date": f"{day} 00:00:00 +0000", "lang": lang,
              "categories": f"[{category}]", "description": "Test", **overrides}
    lines = [f"{key}: {value}" for key, value in fields.items()]
    lines += ["translations:"] + [f"  - lang: {other}" for other in ("en", "de", "es")]
    return "---\n" + "\n".join(lines) + "\n---\n<p class=\"note\">safe</p>\n"


class FrontMatterTests(unittest.TestCase):
    def test_front_matter_splits_header_from_body(self):
        self.assertEqual(health_check.front_matter("---\ntitle: A\n---\nbody\n"), ("title: A\n", "body\n"))

    def test_unclosed_or_absent_front_matter_is_all_body(self):
        for text in ("title: A\nbody\n", "---\ntitle: A\nbody\n"):
            self.assertEqual(health_check.front_matter(text), ("", text))

    def test_scalar_strips_quotes_and_matches_whole_key(self):
        self.assertEqual(health_check.scalar('title:  "A"  \n', "title"), "A")
        self.assertEqual(health_check.scalar("lang: 'en'\n", "lang"), "en")
        self.assertEqual(health_check.scalar("language: de\n", "lang"), "")


class PostContractTests(unittest.TestCase):
    def problems(self, posts: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_posts").mkdir()
            for name, text in posts.items():
                (root / "_posts" / name).write_text(text, encoding="utf-8")
            detail = health_check.post_contracts(root)["detail"]
            return [] if detail == "ok" else detail

    def complete_set(self, **overrides: str) -> dict[str, str]:
        return {f"2026-01-01-{lang}-test.md": article(lang) for lang in ("en", "de", "es")} | overrides

    def test_complete_publication_set_passes(self):
        self.assertEqual(self.problems(self.complete_set()), [])

    def test_each_post_rule_fails_on_its_own(self):
        en = "2026-01-01-en-test.md"
        cases = {
            "filename must be date-lang-lowercase-ascii-slug": {"2026-01-01-en-Bad_Slug.md": article("en")},
            "missing front matter description": {en: article("en").replace("description: Test\n", "")},
            "lang 'de' does not match filename": {en: article("de")},
            "layout must be article": {en: article("en", layout="page")},
            "translations missing es": {en: article("en").replace("  - lang: es\n", "")},
            "missing visible production-protection note": {en: article("en").replace(' class="note"', "")},
        }
        for phrase, override in cases.items():
            with self.subTest(phrase):
                problems = self.problems(self.complete_set(**override))
                self.assertTrue(any(phrase in problem for problem in problems), problems)

    def test_publication_set_needs_every_language_and_some_post(self):
        posts = self.complete_set()
        del posts["2026-01-01-es-test.md"]
        self.assertEqual(self.problems(posts), ["2026-01-01: publication set must contain EN/DE/ES, found ['de', 'en']"])
        self.assertEqual(self.problems({}), ["no canonical posts found"])


class RedirectContractTests(unittest.TestCase):
    TARGET = "/architecture/2026/01/01/en-test/"

    def problems(self, redirect: str, post: str = article("en")) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_posts").mkdir()
            (root / "posts").mkdir()
            (root / "_posts/2026-01-01-en-test.md").write_text(post, encoding="utf-8")
            (root / "posts/old.html").write_text(redirect, encoding="utf-8")
            detail = health_check.redirect_contracts(root)["detail"]
            return [] if detail == "ok" else detail

    def test_redirect_to_a_post_permalink_passes(self):
        self.assertEqual(self.problems(f"---\nlayout: redirect\nredirect_to: {self.TARGET}\n---\n\n"), [])

    def test_redirect_layout_and_site_local_target_are_required(self):
        self.assertEqual(self.problems(f"---\nlayout: article\nredirect_to: {self.TARGET}\n---\n"),
                         ["old.html: layout must be redirect"])
        for target in ("", "https://example.com/new/", "new/"):
            with self.subTest(target=target):
                self.assertEqual(self.problems(f"---\nlayout: redirect\nredirect_to: {target}\n---\n"),
                                 ["old.html: redirect_to must be a site-local canonical path"])

    def test_redirect_must_reach_an_existing_permalink(self):
        for target in ("/tutorial/2026/01/01/en-test/", "/architecture/2026/01/02/en-test/", "/architecture/2026/01/01/en-other/"):
            with self.subTest(target=target):
                self.assertEqual(self.problems(f"---\nlayout: redirect\nredirect_to: {target}\n---\n"),
                                 [f"old.html: redirect_to {target} is not a canonical post permalink"])

    def test_permalink_follows_jekyll_categories_and_overrides(self):
        cases = [
            ("/sap/pm/2026/01/01/en-test/", article("en", category="SAP, pm")),
            ("/sap/pm/2026/01/01/en-test/", article("en", categories="sap pm")),
            ("/architecture/2026/01/01/renamed/", article("en", slug="renamed")),
            ("/fixed/", article("en", permalink="/fixed/")),
            ("/architecture/2026/01/01/en-test/", article("en", date="unparsed")),
        ]
        for target, post in cases:
            with self.subTest(post=post.splitlines()[1:7]):
                self.assertEqual(self.problems(f"---\nlayout: redirect\nredirect_to: {target}\n---\n", post), [])


class BriefTests(unittest.TestCase):
    def test_brief_output_lists_only_failures(self):
        summary = {"failure_count": 1, "checks": [
            {"check": "a", "status": "pass", "detail": "ok"},
            {"check": "b", "status": "fail", "detail": "broken"}]}
        self.assertEqual(health_check.brief(summary), "HEALTH FAIL: 1/2 checks pass\nFAIL b: broken")

    def test_brief_output_counts_skipped_checks_without_listing_them(self):
        summary = {"failure_count": 0, "checks": [
            {"check": "a", "status": "pass", "detail": "ok"},
            {"check": "shell_syntax", "status": "skip", "detail": "bash not found"}]}
        self.assertEqual(health_check.brief(summary), "HEALTH PASS: 1/2 checks pass, 1 skipped")


if __name__ == "__main__":
    unittest.main()
