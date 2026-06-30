#!/bin/sh
# Point this repo at .githooks/ (prepare-commit-msg adds [skip ci] for non-site commits).
set -e
cd "$(dirname "$0")/.."
git config core.hooksPath .githooks
chmod +x .githooks/prepare-commit-msg
echo "Git hooks: core.hooksPath=.githooks (prepare-commit-msg → [skip ci] for .specstory etc.)"
