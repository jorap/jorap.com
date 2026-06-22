#!/usr/bin/env node
/**
 * Install prepare-commit-msg hook (updates CHANGELOG.md on commit).
 * Embeds the absolute Node path — git hooks often run without mise/nvm on PATH.
 */
import fs from "node:fs";
import path from "node:path";
import { projectRoot } from "./spawnUtil.mjs";

const gitDir = path.join(projectRoot, ".git");
if (!fs.existsSync(gitDir)) {
  console.warn("hooks:install skipped (not a git checkout)");
  process.exit(0);
}

const nodeBin = process.execPath.replace(/\\/g, "/");
const hookPath = path.join(gitDir, "hooks", "prepare-commit-msg");
const root = projectRoot.replace(/\\/g, "/");
const hook = `#!/bin/sh
set -e
cd "${root}"
"${nodeBin}" scripts/updateChangelog.mjs "$1"
git add CHANGELOG.md
`;

fs.writeFileSync(hookPath, hook, { mode: 0o755 });
console.log("hooks: installed prepare-commit-msg → CHANGELOG.md");
