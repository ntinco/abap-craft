# Jekyll Post Front Matter Template

Use this template for canonical post files under `_posts/`.

```yaml
---
layout: article
title: "<localized title>"
date: YYYY-MM-DD 00:00:00 +0000
lang: en
categories: [architecture]
description: "<short architecture-focused summary>"
og_description: "<optional override for OG>"
twitter_description: "<optional override for Twitter>"
back_label: "Back to ABAP Craft"
discuss_label: "Discuss this article"
comments_intro: "Comments are powered by GitHub Discussions."
translations:
  - lang: en
    label: English
    url: /architecture/YYYY/MM/DD/en-<slug>/
  - lang: de
    label: Deutsch
    url: /architecture/YYYY/MM/DD/de-<slug>/
  - lang: es
    label: Espanol
    url: /architecture/YYYY/MM/DD/es-<slug>/
---
```

Notes:

- Keep filenames lowercase and ASCII-only.
- Keep `lang` and `translations` fully aligned.
- Update label and intro strings for DE and ES localized versions.
