#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = {"en", "de", "es"}
REQUIRED = [
    "AGENTS.md", "README.md", "ai/governance.md", "ai/repo-map.json",
    "_posts", "_layouts/article.html", "_layouts/redirect.html", "index.html", "posts.md", "_config.yml",
    "posts", "prompts/README.md", "prompts/editorial-voice.md", "prompts/templates",
    "tools/health_check.py", "tests/test_health_check.py", ".github/workflows/jekyll-gh-pages.yml",
]
FORBIDDEN_CONTROL = [
    ".github/copilot-instructions.md",
    "prompts/abap-keyflow-writing-prompt.md",
    "prompts/abap-keyflow-publishing-prompt.md",
    "prompts/system",
    "prompts/workflows",
    "prompts/operations",
    "prompts/checklists",
    "prompts/simulations",
    "docs/rag-content-strategy.md",
    "docs/simple-content-system.md",
]
TEXT_SUFFIXES = {".md", ".html", ".json", ".py", ".yml", ".yaml", ".css", ".js", ".xml", ".txt"}
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential_assignment": re.compile(r"(?i)\b(?:password|passwd|token|secret)\s*[=:]\s*[^\s${}<]{8,}"),
}


def result(name: str, problems: list[str]) -> dict[str, object]:
    return {"check": name, "status": "fail" if problems else "pass", "detail": problems or "ok"}


def required_paths(root: Path) -> dict[str, object]:
    return result("required_paths", [p for p in REQUIRED if not (root / p).exists()])


def forbidden_surfaces(root: Path) -> dict[str, object]:
    return result("forbidden_control_surfaces", [p for p in FORBIDDEN_CONTROL if (root / p).exists()])


def repo_map(root: Path) -> dict[str, object]:
    problems: list[str] = []
    try:
        data = json.loads((root / "ai/repo-map.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return result("repo_map", [str(exc)])
    if data.get("schema_version") != "1.0":
        problems.append("schema_version must be 1.0")
    routing = data.get("routing")
    if not isinstance(routing, dict):
        problems.append("routing must be an object")
        routing = {}
    for task, paths in routing.items():
        if not isinstance(paths, list) or not paths:
            problems.append(f"routing {task!r} must contain paths")
            continue
        for routed in paths:
            if not (root / str(routed).rstrip("/")).exists():
                problems.append(f"{task}: missing routed path {routed}")
    return result("repo_map", problems)


def front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return "", text
    return parts[1], parts[2]


def scalar(fm: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", fm)
    return match.group(1).strip().strip('"\'') if match else ""


def post_contracts(root: Path) -> dict[str, object]:
    problems: list[str] = []
    by_date: dict[str, set[str]] = defaultdict(set)
    posts = sorted((root / "_posts").glob("*.md"))
    if not posts:
        problems.append("no canonical posts found")
    for path in posts:
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-(en|de|es)-([a-z0-9-]+)\.md", path.name)
        if not match:
            problems.append(f"{path.name}: filename must be date-lang-lowercase-ascii-slug")
            continue
        day, filename_lang, _ = match.groups()
        fm, body = front_matter(path.read_text(encoding="utf-8"))
        for key in ("layout", "title", "date", "lang", "categories", "description", "translations"):
            if not re.search(rf"(?m)^{re.escape(key)}:", fm):
                problems.append(f"{path.name}: missing front matter {key}")
        lang = scalar(fm, "lang")
        if lang != filename_lang:
            problems.append(f"{path.name}: lang {lang!r} does not match filename")
        if scalar(fm, "layout") != "article":
            problems.append(f"{path.name}: layout must be article")
        by_date[day].add(filename_lang)
        for required_lang in LANGS:
            if not re.search(rf"(?m)^\s*- lang:\s*{required_lang}\s*$", fm):
                problems.append(f"{path.name}: translations missing {required_lang}")
        if 'class="note"' not in body:
            problems.append(f"{path.name}: missing visible production-protection note")
    for day, langs in by_date.items():
        if langs != LANGS:
            problems.append(f"{day}: publication set must contain EN/DE/ES, found {sorted(langs)}")
    return result("post_contracts", problems)


def redirect_contracts(root: Path) -> dict[str, object]:
    problems: list[str] = []
    for path in sorted((root / "posts").glob("*.html")):
        fm, body = front_matter(path.read_text(encoding="utf-8"))
        if scalar(fm, "layout") != "redirect":
            problems.append(f"{path.name}: layout must be redirect")
        if not scalar(fm, "redirect_to").startswith("/"):
            problems.append(f"{path.name}: redirect_to must be a site-local canonical path")
        if body.strip():
            problems.append(f"{path.name}: redirect must not duplicate article body")
    return result("redirect_contracts", problems)


def secret_scan(root: Path) -> dict[str, object]:
    problems: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                problems.append(f"secret-like content: {rel}:{name}")
    return result("secret_scan", problems)


WORKSPACE_CONTRACT = re.compile(r"<!-- workspace-contract sha256:(\S+) -->\n(.*?)<!-- /workspace-contract -->", re.DOTALL)


def workspace_contract_problems(root: Path) -> list[str]:
    """The shared workspace contract block is present once and unedited, and the rules it sets are wired."""
    problems: list[str] = []
    governance = root / "ai/governance.md"
    source = governance.read_text(encoding="utf-8").replace("\r\n", "\n") if governance.is_file() else ""
    blocks = WORKSPACE_CONTRACT.findall(source)
    if len(blocks) != 1:
        problems.append(f"ai/governance.md needs one workspace contract block, found {len(blocks)}")
    elif hashlib.sha256(blocks[0][1].encode("utf-8")).hexdigest()[:12] != blocks[0][0]:
        problems.append("workspace contract edited here: edit it in gen-box and run tools/contract_sync.py")
    try:
        pending = json.loads((root / "ai/repo-map.json").read_text(encoding="utf-8")).get("pending_acceptance")
    except (OSError, json.JSONDecodeError):
        pending = None
    if not isinstance(pending, str) or not pending.strip():
        problems.append("ai/repo-map.json must name one pending_acceptance path")
    claude = root / "CLAUDE.md"
    if not claude.is_file() or claude.read_text(encoding="utf-8").strip() != "@AGENTS.md":
        problems.append("CLAUDE.md must exist and contain only @AGENTS.md")
    if not (root / ".githooks/pre-commit").is_file():
        problems.append(".githooks/pre-commit is missing")
    return problems


def workspace_contract(root: Path) -> dict[str, object]:
    return result("workspace_contract", workspace_contract_problems(root))


def build(root: Path = ROOT) -> dict[str, object]:
    checks = [required_paths(root), forbidden_surfaces(root), repo_map(root), post_contracts(root), redirect_contracts(root), secret_scan(root), workspace_contract(root)]
    failures = sum(c["status"] == "fail" for c in checks)
    return {"structural_status": "fail" if failures else "pass", "failure_count": failures, "checks": checks}


def brief(summary: dict) -> str:
    failed = [c for c in summary["checks"] if c["status"] != "pass"]
    status = "FAIL" if summary["failure_count"] else "PASS"
    lines = [f"HEALTH {status}: {len(summary['checks']) - len(failed)}/{len(summary['checks'])} checks pass"]
    lines += [f"{c['status'].upper()} {c['check']}: {c['detail']}" for c in failed]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true", help="print every check as JSON")
    args = parser.parse_args()
    summary = build()
    print(json.dumps(summary, indent=2) if args.json else brief(summary))
    return 1 if summary["failure_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
