# ABAP Craft AI Governance

## Identity

ABAP Craft is a human-owned publication, an AI-operated publishing system, and a human-facing public artifact.

AI-first optimization applies to the control plane. It must not make the repository unauditable, non-deterministic, unrecoverable, or dependent on a specific AI provider. Public output remains optimized for human readers because readers are the consumer of the artifact plane.

## Ownership

Human-owned:
- lived/project experience and factual claims about that experience;
- architectural position, opinions and conclusions attributed to the author;
- editorial voice and materially consequential positioning;
- publication acceptance when claims or positioning materially change.

AI-operated:
- article structure and draft implementation after intent/evidence is supplied;
- front matter, translations and translation parity;
- internal links, redirects, formatting and publication mechanics;
- repository navigation, maintenance, validation and control-plane consistency.

## Read routing

1. Read `ai/repo-map.json` after this file.
2. For content work, read the source material supplied/approved by the human, `prompts/editorial-voice.md`, the relevant post(s), and only the templates/layouts needed by the task.
3. For translation work, treat the approved source-language article as the claims authority; preserve argument and technical meaning.
4. For publishing mechanics, inspect `_posts/`, `_layouts/`, `index.html`, `posts.md`, `_config.yml` and `posts/` only as required.
5. Do not load historical simulations or deprecated prompt systems; Git history is enough.

## Change routing

- Canonical article content -> `_posts/*.md`.
- Human-owned editorial voice/positioning -> `prompts/editorial-voice.md` only when explicitly changed by the human.
- Reusable input/front-matter shapes -> `prompts/templates/`.
- Site presentation -> `_layouts/`, `index.html`, `posts.md`, assets/config as applicable.
- Compatibility redirect -> `posts/*.html`; never duplicate article bodies there.
- AI operating rules -> `ai/governance.md`.
- Machine routing -> `ai/repo-map.json`.

Do not create a second source of truth for article content or publishing policy.

## Evidence discipline

Never invent and attribute to the author:
- experiences or production situations;
- metrics or customer outcomes;
- opinions or architectural conclusions;
- technical patterns the source material does not support.

If a stronger claim would require unsupported evidence, omit it or request human input. Protect production/customer information: no real client/company names, live system identifiers, internal URLs, credentials, private payloads, ticket identifiers, colleague names or other identifying details unless explicitly safe and intended for publication.

Generic/anonymized examples such as `ZXX_*`, `SYSTEM_A`, `SYSTEM_B`, `MIDDLEWARE`, `TX01` and `TX02` are acceptable when they cannot identify a real environment.

## Publication invariants

- `_posts/*.md` is canonical article content.
- Published article sets currently maintain EN/DE/ES variants with the same architectural argument and symmetric translation links.
- English is the default source language unless the human explicitly chooses another workflow.
- Slugs are lowercase ASCII and hyphenated.
- Front matter must remain compatible with `_layouts/article.html`.
- Redirect files contain redirect front matter only and point to canonical article routes.
- Public URLs should remain stable when practical.
- Do not machine-score editorial quality; validate mechanical publication contracts only.

## Editorial input

`prompts/editorial-voice.md` captures voice and positioning that are genuinely human-owned and costly to reconstruct. It is editorial input, not a second governance surface. Templates are reusable shapes, not policy.

## Security and privacy

No passwords, tokens, private keys, live credentials, private `.env`, customer/internal URLs or production-identifying private data belong in the repository. Public URLs intentionally used by the publication are allowed.

## Completion

For material content changes, preserve author intent and obtain human acceptance before treating changed personal/architectural claims as final. For mechanical publishing changes, AI may complete autonomously when validation passes.

Run:

```bash
python3 -m unittest discover -s tests
python3 tools/health_check.py --strict
```

The existing GitHub Pages workflow remains the build/deploy validation for the public artifact.

<!-- workspace-contract sha256:885e0973f8f7 -->
## Workspace contract

Identical in the six repositories under `~/gh/`. The master copy is the one in
`gen-box/ai/governance.md`: edit only that one, then run `python3 tools/contract_sync.py ~/gh` from `gen-box`.
Two of the repositories are public, so this section never holds private detail.

Precedence, highest first:

1. The human's explicit instruction in the session. Name the rule it overrides; a lasting change is written into the file that owns the rule.
2. This contract, for anything that crosses repositories: routing, data class, autonomy.
3. The rest of the repository's `ai/governance.md`, for anything inside it.
4. `ai/repo-map.json`: it locates and runs things and sets no rule.
5. Skills and templates, always optional.

`AGENTS.md` and `CLAUDE.md` only point here. When a text and a validator disagree, the failing validator is the
current truth: fix the rule or the code, never ignore the failure.

| Repo | Holds | Data class |
|---|---|---|
| `ntinco-os` | personal operating system: state, plans, time, finance, durable context | private-personal |
| `abap-box` | ABAP/SAP technical memory: knowledge, cheatsheets, skills, SAP utilities | private-technical |
| `abap-craft` | ABAP Craft, the public ABAP articles site | public |
| `gen-box` | generic reusable tools and agent skills | private-technical |
| `keyflow` | hotkeys, hotstrings and daily desktop automation (Windows/macOS) | public |
| `keyflow-station` | workstation installation, maintenance and backup sync | private-technical |

Content only moves to a repository of the same or a more private class, with one exception below.
Private-personal content never leaves `ntinco-os`. Client or employer confidential data belongs in none of them.

Routing between repositories:

- Generic tool or file converter -> `gen-box`; other repositories run it from `~/gh/gen-box/tools/` and never copy it.
- ABAP/SAP knowledge -> `abap-box`; to `abap-craft` only anonymized and with explicit human approval.
- Hotkey, hotstring or daily desktop automation -> `keyflow`.
- Installation, provisioning or machine maintenance -> `keyflow-station`.
- Personal fact, plan, time or finance -> `ntinco-os`.
- When a task belongs to another repository, say so and work there; never build a local substitute.

Autonomy:

- Without asking: read, edit, run validators and commit on the task branch.
- Ask first: push, open a pull request, or change a repository other than the task's.
- Only on explicit human order: merge or push to `main`; delete branches, tags, stashes, untracked files or remote data;
  rewrite published history (rebase, amend, force push).

Parallel work: one branch or worktree per task (`git worktree add ../<repo>-<task> -b <task>`). Never stage, commit,
stash, reset or revert changes you did not make; if the tree holds foreign changes, use a new worktree.

Pending acceptance: what waits for the human (runtime checks, claims to confirm) lives in one place per repository,
declared in `ai/repo-map.json` -> `pending_acceptance`; that file may be absent while nothing is pending.

Commands: write `python3` in commands and docs. Validators that need a specific OS or application (AutoHotkey,
Hammerspoon, PowerShell, SAP) go in `ai/repo-map.json` -> `platform_validators` and never run in CI on another platform.
Hooks: enable the versioned hooks once per clone with `git config core.hooksPath .githooks` (a Claude Code
SessionStart hook in `.claude/settings.json` may do it); the pre-commit hook runs the health check on the staged tree.
`gen-box/tools/secret_guard.py` is the Claude Code PreToolUse hook (matcher `Bash`) that extends the Read/Edit deny
list to shell commands; the human wires it in `.claude/settings.json`.
Hooks and validators execute repository code: run them only on branches the human or their agents wrote, and review an
outside contribution in CI or a disposable environment first. `CLAUDE.md` only imports `AGENTS.md`; it is never a
second authority.
<!-- /workspace-contract -->
