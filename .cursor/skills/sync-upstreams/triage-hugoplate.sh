#!/usr/bin/env bash
# Classify Hugoplate vs JoRap theme diffs before applying anything.
# Run from jorap.com root. Read-only — does not copy files.
set -euo pipefail

HUGO="${HUGO:-../hugoplate}"
THEME="themes/jorap"
EXCLUDES=".cursor/skills/sync-upstreams/hugoplate-rsync-excludes.txt"

if [[ ! -d "$HUGO" ]]; then
  echo "Missing Hugoplate checkout: $HUGO" >&2
  exit 1
fi

is_excluded() {
  local rel="$1"
  local short="$rel"
  short="${short#layouts/}"
  short="${short#assets/}"
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    if [[ "$rel" == "$line" || "$rel" == "$line/"* \
       || "$short" == "$line" || "$short" == "$line/"* \
       || "$short" == "$line"* ]]; then
      return 0
    fi
  done < "$EXCLUDES"
  return 1
}

red_flags_in_diff() {
  local diff_file="$1"
  grep -Eqi \
    'text-ink|bg-surface|border-divider|semantic-tokens|self-hosted-fonts|theme-init|heading-title-case|article-title|header-offset|color-scheme|--color-ink|partial "essentials/self-hosted|partial "components/icon|partial "components/social-share|nav-dropdown-trigger|cspHashes|theme-name.*jorap|gallery-slider|home-intro|home-scope|home-proof|home-writing|spotify|youtube_time' \
    "$diff_file" 2>/dev/null
}

upstream_regression_flags() {
  local diff_file="$1"
  grep -Eqi \
    'theme-name.*hugoplate|fonts\.googleapis\.com|use\.fontawesome\.com|fa-regular|fa-solid|text-text-dark|bg-body|dark:bg-darkmode|dark:text-darkmode' \
    "$diff_file" 2>/dev/null
}

classify_pair() {
  local src="$1"
  local rel="${src#"$HUGO"/}"
  local dst="$THEME/$rel"

  if is_excluded "$rel"; then
    echo "BLOCKED|$rel|On preserve/exclude list"
    return
  fi

  if [[ ! -e "$dst" ]]; then
    echo "ADD-ONLY|$rel|New upstream file — safe to add if not JoRap-specific path"
    return
  fi

  if diff -q "$src" "$dst" >/dev/null 2>&1; then
    return
  fi

  local tmp
  tmp="$(mktemp)"
  diff -u "$dst" "$src" > "$tmp" || true

  if red_flags_in_diff "$tmp"; then
    echo "MANUAL|$rel|JoRap customization detected — merge by hand or skip"
  elif upstream_regression_flags "$tmp"; then
    echo "SKIP|$rel|Would revert JoRap tokens, fonts, or CSP-friendly setup"
  else
    echo "CANDIDATE|$rel|Likely safe — still read diff before copying"
  fi

  rm -f "$tmp"
}

echo "=== Hugoplate triage (read-only) ==="
echo "Upstream: $HUGO"
echo "Theme:    $THEME"
echo

blocked=0 manual=0 skip=0 candidate=0 add=0

while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  result="$(classify_pair "$path")"
  [[ -z "$result" ]] && continue
  echo "$result" | tr '|' '\t'
  case "${result%%|*}" in
    BLOCKED) blocked=$((blocked + 1)) ;;
    MANUAL) manual=$((manual + 1)) ;;
    SKIP) skip=$((skip + 1)) ;;
    CANDIDATE) candidate=$((candidate + 1)) ;;
    ADD-ONLY) add=$((add + 1)) ;;
  esac
done < <(find "$HUGO/layouts" "$HUGO/assets" -type f 2>/dev/null | sort)

echo
echo "Summary: BLOCKED=$blocked MANUAL=$manual SKIP=$skip CANDIDATE=$candidate ADD-ONLY=$add"
echo "Apply only CANDIDATE and ADD-ONLY after reading each diff. Never bulk-rsync CSS, JS, or core layouts."
