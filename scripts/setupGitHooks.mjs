#!/usr/bin/env node
/** Point repo at .githooks/ (prepare-commit-msg adds [skip ci] for non-site commits). */
import { chmodSync } from "node:fs";
import { join } from "node:path";
import { projectRoot, run } from "./spawnUtil.mjs";

run("git", ["config", "core.hooksPath", ".githooks"]);

const hook = join(projectRoot, ".githooks", "prepare-commit-msg");
if (process.platform !== "win32") {
  chmodSync(hook, 0o755);
}

console.log(
  "Git hooks: core.hooksPath=.githooks (prepare-commit-msg → [skip ci] for .specstory etc.)",
);
