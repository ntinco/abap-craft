# ABAP Keyflow AI Governance

## Identity

ABAP Keyflow is a human-owned publication, an AI-operated publishing system, and a human-facing public artifact.

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
python -m unittest discover -s tests -v
python tools/health_check.py --strict
```

The existing GitHub Pages workflow remains the build/deploy validation for the public artifact.
