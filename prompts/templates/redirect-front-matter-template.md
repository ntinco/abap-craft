# Redirect Front Matter Template

Use this template for legacy URL redirects under `posts/`.

```yaml
---
layout: redirect
title: "Redirecting to the canonical ABAP Craft article"
redirect_to: /architecture/YYYY/MM/DD/en-<slug>/
---
```

Notes:

- Keep redirect pages minimal.
- Point redirects to canonical Jekyll routes.
- Use one redirect file per legacy public URL that must be preserved.
