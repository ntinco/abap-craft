# ABAP Keyflow

ABAP Keyflow is a public knowledge base about SAP PM, ABAP architecture, integration design, maintainability, and how large custom codebases degrade over time.

It exists for two reasons:

- to make senior-level ABAP architecture work visible to an international audience
- to turn real project experience into reusable, structured context that remains useful over time

Website:

`https://nor001.github.io/ABAP_Keyflow/`

## What this repository is

This is not a tutorial repository.

It is a technical publishing repository focused on practical architecture lessons from real SAP systems, especially the kind of lessons that appear after years of integrations, change requests, custom development, and team rotation.

The project is intentionally simple:

- one public site
- one content source of truth
- one clear publishing flow
- minimal moving parts

## What the project tries to show

ABAP Keyflow is designed to show more than coding ability.

It is meant to show:

- architectural judgment
- maintainability thinking
- responsibility boundaries
- integration discipline
- long-term reasoning in SAP custom code
- the ability to structure knowledge for both humans and AI

## Operating model

The repository is **human-owned, AI-maintained, human-readable**.

The author owns intent, architectural judgment, lived experience, editorial voice and publication acceptance. AI is the primary maintenance executor for repository consistency, translations, metadata, publishing mechanics, validation and structural upkeep. AI must not invent experience or conclusions on the author's behalf, and the repository must remain directly understandable without requiring AI reconstruction.

## Main topics

- ABAP architecture
- SAP PM custom development
- integration design
- architectural drift
- class responsibility boundaries
- naming conventions that expose architecture
- maintainability in legacy SAP systems
- technical leadership in rotating teams
- AI-assisted documentation and publishing

## Audience

This repository is primarily for:

- senior ABAP developers
- SAP technical leads
- integration-heavy SAP teams
- clients or hiring managers evaluating architectural maturity
- AI agents that need stable repository context

## Repository structure

- `_posts/`: canonical article source in Markdown
- `index.html`: Jekyll-rendered homepage
- `posts/`: legacy redirect pages for old public URLs
- `posts.md`: article listing page
- `prompts/`: writing, publishing, and prompt-system support files
- `AGENTS.md`: operational rules for AI agents working in this repository

## Operating principles

This repository prefers:

- simplicity over completeness
- one source of truth over duplicated convenience
- human readability alongside AI-maintained consistency
- stable structure over fast expansion
- editing existing files before creating new ones

## Publishing model

The site uses Jekyll and GitHub Pages.

The source of truth for articles is `_posts/*.md`.

Legacy files under `posts/` should exist only when an old public URL must keep working.

The repository may include prompts and AI support material, but those should support the content system, not replace it.

## Why this matters

Modern teams are using more AI to generate, accelerate, and restructure work. That creates a new risk: systems become more complex, but the reasoning behind them becomes less visible.

ABAP Keyflow exists in part to fight that problem.

The goal is to keep architecture, decisions, and technical judgment understandable enough that both a human and an AI agent can continue the work without guessing.
