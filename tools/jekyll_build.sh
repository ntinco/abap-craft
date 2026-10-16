#!/bin/sh
# Builds the site with the image the GitHub Pages workflow uses (actions/jekyll-build-pages@v1), without deploying.
# Needs Docker and network access (remote theme). The source is mounted read-only and the output stays in the container.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
# A source the Docker daemon cannot see mounts empty and would build an empty site: fail on it instead.
exec docker run --rm --platform linux/amd64 -v "$root":/src:ro \
  -e JEKYLL_ENV=production -e PAGES_REPO_NWO=ntinco/abap-craft \
  --entrypoint /bin/sh ghcr.io/actions/jekyll-build-pages:v1.0.13 \
  -c 'test -f /src/_config.yml && exec /usr/local/bundle/bin/github-pages build --source /src --destination /tmp/_site'
