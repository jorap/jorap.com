#!/usr/bin/env bash
# Cloudflare Pages — set dashboard build command to: bash scripts/cf-pages-build.sh
set -euo pipefail
npm run project-setup
npm run update-modules
exec hugo --gc --minify --templateMetrics --templateMetricsHints --forceSyncStatic -b "${CF_PAGES_URL:-/}"
