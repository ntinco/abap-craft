# AGENTS.md

This file defines how AI agents should work in `ABAP_Keyflow`.

## Operating model

This repository is **human-owned, AI-maintained, human-readable**.

- The human owns intent, architectural judgment, lived project experience, editorial voice, publication decisions, and final acceptance.
- AI is the primary technical and editorial maintainer for repository consistency, implementation, refactoring, translation parity, publishing mechanics, validation, and maintenance of these instructions.
- AI must not invent experiences, opinions, metrics, production outcomes, or architectural conclusions and attribute them to the author.
- Optimizing maintenance for AI must never make the repository dependent on AI for direct human understanding or reuse.

The repository should stay simple, readable, and easy to maintain.

## Core intent

This repository has two jobs:

1. Make the author's ABAP and SAP architecture thinking visible to a global audience.
2. Preserve enough structured context that future work can be continued by humans or AI without unnecessary guessing.

## Read this first

Before making content changes, an agent should inspect:

1. `README.md`
2. `AGENTS.md`
3. `prompts/abap-keyflow-writing-prompt.md`
4. `prompts/abap-keyflow-publishing-prompt.md`
5. one current article in `_posts/`

Do not start by inventing a new structure.

## Non-goals

Do not turn this repository into a complex documentation system.

Avoid:

- unnecessary files
- unnecessary folders
- duplicated sources of truth
- hidden automation
- process for the sake of process

## Source of truth

- Articles live in `_posts/*.md`.
- `index.html` is the Jekyll-rendered homepage.
- `posts/*.html` are legacy redirect pages only.
- Public-facing project context lives in `README.md`.
- Agent operating rules live in `AGENTS.md`.

If a change would create a second source of truth, do not do it.

## Change policy

When editing this repository:

- prefer editing existing files over creating new files
- create a new file only when the current file is clearly overloaded
- keep structure boring and obvious
- keep public URLs stable when practical
- preserve backward compatibility for article links where possible
- use AI to remove maintenance friction, not to add abstraction or process

## Simplicity rules

Apply these principles:

- KISS: choose the simplest structure that still works
- YAGNI: do not add future-facing documentation layers before they are needed
- DRY: avoid duplication of meaning, not just duplication of text

Important:

Do not misuse DRY to split context into many tiny files.

In this repository, readability is often more important than aggressive decomposition.

## Current content model

At the moment, the live article set is intentionally small:

- one English article
- one German article
- one Spanish article

Older `_posts` drafts or duplicate source files should remain unpublished unless they are intentionally being revived.

## Content rules

Articles should stay aligned with the project purpose:

- real architectural tension over generic tutorials
- practical tradeoffs over broad theory
- maintainability over novelty
- anonymized production reality over specific client detail

Every article should protect production information.

Use placeholders such as:

- `ZXX_*`
- `SYSTEM_A`
- `SYSTEM_B`
- `MIDDLEWARE`
- `TX01`
- `TX02`

## Article workflow

When creating or updating an article:

1. Start from a real architectural lesson or tradeoff supplied or approved by the human owner.
2. Write the English source first unless the user explicitly wants another order.
3. Keep front matter complete and consistent.
4. Preserve or add:
   - `title`
   - `date`
   - `lang`
   - `categories`
   - `tags`
   - `permalink`
   - `description`
   - translation links
5. Keep the tone senior, direct, and architecture-focused.
6. Never add unsupported claims, invented metrics, production-identifying details, or fabricated personal experience.

## Translation workflow

When working across EN, DE, and ES:

- preserve the same architectural argument in all languages
- adapt wording, not meaning
- keep permalinks language-specific
- keep translation links symmetrical
- do not let one version drift structurally from the others without reason

If one version is updated materially, check whether the other two now need parity updates.

## Homepage workflow

The homepage should remain simple.

It should:

- explain the project clearly
- highlight the most important content
- avoid becoming a second manual content database

When updating `index.html`:

- keep the language switcher working
- keep featured article links aligned with the text shown beside them
- avoid hardcoding copy that will become wrong when a new featured article is added
- make sure list sections behave correctly as more articles are added

## Redirect workflow

Files under `posts/` are not canonical article content.

Touch them only when:

- an old public URL must be preserved
- a canonical permalink changes
- a new public compatibility redirect is required

Do not rebuild full article HTML manually inside `posts/`.

## Publishing rules

Before publishing:

- keep front matter complete and consistent
- preserve language metadata
- preserve canonical permalinks
- preserve article-to-article translation links
- ensure redirects still point to canonical article pages
- make sure homepage links still match live content
- verify that no production-identifying detail or unsupported personal claim was introduced

## When to create more structure

Do not add more documentation files unless one of these becomes true:

- `README.md` becomes too public-facing to carry operational context
- `AGENTS.md` becomes too large to stay usable
- publishing work becomes repetitive enough that one dedicated file would remove real friction

Until then, keep the repository minimal.

## Preferred agent behavior

Agents working here should:

- act as the primary maintenance executor once human intent is clear
- make small, understandable changes
- maintain translation, metadata, links, redirects and publishing consistency proactively within scope
- explain structure through code and file organization, not through complexity
- avoid inventing conventions that are not already established
- preserve direct human readability and the author's voice
- use AI support to reduce friction, not to add abstraction
