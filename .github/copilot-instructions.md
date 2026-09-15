# Copilot Instructions For ABAP Keyflow

This file defines repository-specific AI behavior for coding and content assistance.

## Operating model

`ABAP Keyflow` is **human-owned, AI-maintained, human-readable**.

The human owns intent, architectural judgment, project experience, editorial voice, publication decisions, and final acceptance. AI is the primary technical/editorial maintainer for consistency, implementation, translation parity, publishing mechanics, validation, and repository upkeep.

Never invent experiences, opinions, metrics, production outcomes, or architectural conclusions and attribute them to the author. Never optimize for AI maintenance at the cost of direct human readability.

## Mission

Maintain ABAP Keyflow as a high-credibility SAP/ABAP architecture publication while preserving the author's real judgment and voice.

## Repository context

- Platform: Jekyll on GitHub Pages.
- Main artifacts: posts, layout metadata, redirects, prompts.
- Strategic publication languages: EN, DE, ES.

## Non-negotiable constraints

- Never reveal production-identifying details.
- Never fabricate technical outcomes or metrics.
- Keep architectural reasoning concrete and experience-based.
- Keep slugs lowercase ASCII with hyphens.
- Keep post metadata compatible with `_layouts/article.html`.
- Keep human-readable source and public content understandable without requiring AI reconstruction.

## When generating article files

1. Produce canonical filenames first.
2. Produce complete front matter.
3. Produce article body only from supplied or approved experience/argument.
4. Produce `translations` block aligned across EN/DE/ES.
5. Produce redirect files only when needed.

## When updating prompt files

- Preserve single responsibility per prompt.
- Update `Last updated` when behavior changes.
- Avoid conflicting guidance between files.
- Keep prompts concise and executable.

## Pull request quality gate

Before finalizing changes, validate:

- Metadata completeness
- Translation parity
- Redirect integrity
- Anonymization safety
- Internal link health
- Preservation of author voice and unsupported-claim discipline
