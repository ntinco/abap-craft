# Editorial voice

Human-owned editorial and positioning guidance for ABAP Keyflow. Operational, privacy and publishing rules live in `ai/governance.md`; this file should not duplicate them.

## Positioning

Write as a senior SAP/ABAP practitioner for peers and for an international architecture audience, especially European SAP markets. The publication should demonstrate architectural judgment rather than tutorial coverage.

Primary topics include ABAP architecture, SAP PM custom development, integration design, maintainability, architectural drift, responsibility boundaries, Clean ABAP and AI-assisted documentation/publishing when grounded in real work.

## Core editorial lens

Start from a real architectural lesson or tradeoff supplied or approved by the author. Find the decision beneath the surface topic.

Examples of the desired move:

- surface: class naming -> decision: make responsibility boundaries visible enough to resist architectural drift;
- surface: integration class design -> decision: separate API contract ownership from HTTP transport ownership;
- surface: SAP PM enhancement classes -> decision: distinguish SAP-initiated flows from external-system-initiated flows.

The article should explain what broke or became costly, the tradeoff that mattered, what changed, and why that mattered at scale.

## Default article shape

Use this only when it serves the material; it is not a mandatory parser contract.

1. Outcome-oriented title.
2. Opening from a repeated real-world pattern, not theory.
3. The real problem and its maintainability/onboarding/debugging/regression cost.
4. Two to four decisions or tradeoffs that had to be defended.
5. A concrete scale view: before/after inventory, diagram, taxonomy or structure.
6. A repeatable heuristic/test the reader can use.
7. A concise architecture-focused final lesson.

## Tone

Use:
- direct language;
- precise claims;
- practical examples;
- short clear paragraphs;
- architecture reasoning visible enough for senior peers to challenge.

Avoid:
- generic tutorial voice;
- filler introductions;
- textbook explanations that do not advance the argument;
- novelty for its own sake;
- unsupported certainty.

The target sound is:

> This is what broke, this is the tradeoff, this is what I changed, and this is why it mattered at scale.

not:

> Today we are going to learn about clean code principles.

## Title strategy

Prefer experience/outcome titles such as:
- `How I stopped X`;
- `How I separated X from Y`;
- `Why I stopped doing X`.

Avoid generic `Guide to`, `Introduction to`, or `Best practices for` framing unless the author explicitly wants a reference/tutorial piece.

## Length and depth

For a full architecture article, roughly 1000–1500 words is a useful default, not a quota. Expand only where the tradeoff needs depth. Do not inflate with generic SAP/ABAP explanation.

## Technical language

Keep internationally standard SAP/ABAP terms precise. Do not over-translate labels such as ABAP, SAP PM, API, CLIENT, SERVICE, FACADE, EXT, IDoc, HTTP, payload, clean code or architectural drift when the standard term is clearer.

## Multilingual voice

English is the default source-language voice. German and Spanish versions should preserve the same architectural argument and claim strength while using natural idiomatic phrasing. Translation is adaptation of wording, not invention of new conclusions.

## Distribution copy

When requested, LinkedIn/dev.to copy should remain direct, professional and architecture-focused rather than clickbait. For German-market positioning, emphasize maintainability, documentation discipline, responsibility boundaries and integration ownership when those claims are genuinely supported by the article.

## Quality bar

A strong article should leave a technically informed reader with evidence that the author understands how SAP custom code degrades over time and how to create boundaries that survive change and team rotation.

A weak article merely demonstrates familiarity with a surface technique.
