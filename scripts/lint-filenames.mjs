#!/usr/bin/env node
/**
 * Cross-platform filename safety lint (.cursor/rules/safe-filenames.mdc).
 *
 * Usage:
 *   node scripts/lint-filenames.mjs            # git-tracked paths (default)
 *   node scripts/lint-filenames.mjs --self-check
 *   node scripts/lint-filenames.mjs --walk       # working tree (incl. untracked)
 */
import { spawnSync } from "node:child_process";
import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { projectRoot } from "./spawnUtil.mjs";

const FORBIDDEN = new Set('<>:"|?*\\/');
const RESERVED = new Set([
  "CON",
  "PRN",
  "AUX",
  "NUL",
  ...Array.from({ length: 9 }, (_, i) => `COM${i + 1}`),
  ...Array.from({ length: 9 }, (_, i) => `LPT${i + 1}`),
]);

const SKIP_DIRS = new Set([
  ".git",
  "node_modules",
  "public",
  "resources",
  ".pnpm-store",
  ".cache",
]);

/** @returns {string[]} */
export function checkFilenameComponent(name) {
  const issues = [];
  if (!name) {
    issues.push("empty name");
    return issues;
  }
  if (name !== name.trim()) issues.push("leading/trailing whitespace");
  if (name.endsWith(" ") || name.endsWith(".")) {
    issues.push("trailing space or dot");
  }
  for (const c of name) {
    if (FORBIDDEN.has(c)) {
      issues.push(`forbidden char: ${JSON.stringify(c)}`);
      break;
    }
    if (c.charCodeAt(0) < 32) {
      issues.push("control character");
      break;
    }
  }
  if (name.includes("\0")) issues.push("null byte");

  let stem = name;
  if (name.includes(".") && !name.startsWith(".")) {
    stem = name.slice(0, name.lastIndexOf("."));
  } else if (name.startsWith(".") && name.includes(".", 1)) {
    stem = name.slice(1, name.lastIndexOf("."));
  }
  if (RESERVED.has(stem.toUpperCase())) {
    issues.push(`Windows reserved name: ${stem.toUpperCase()}`);
  }

  if (new TextEncoder().encode(name).length > 200) {
    issues.push("name too long (>200 bytes)");
  }
  return issues;
}

function gitTrackedFiles() {
  const result = spawnSync("git", ["ls-files", "-z"], {
    cwd: projectRoot,
    encoding: "buffer",
  });
  if (result.status !== 0) {
    console.error("git ls-files failed — run from the repo root with git installed.");
    process.exit(1);
  }
  return result.stdout.toString("utf8").split("\0").filter(Boolean);
}

function walkTree(dir, hits) {
  let scanned = 0;
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry) || entry.startsWith(".specstory")) continue;
    scanned += 1;
    const full = join(dir, entry);
    const rel = full.slice(projectRoot.length + 1).replace(/\\/g, "/");
    const st = statSync(full);
    const issues = checkFilenameComponent(entry);
    if (issues.length) hits.push({ path: rel, component: entry, issues });
    if (st.isDirectory()) scanned += walkTree(full, hits);
  }
  return scanned;
}

function runSelfCheck() {
  const cases = [
    ["good-file.md", []],
    ["my-note-title.md", []],
    ["con.md", ["Windows reserved name: CON"]],
    ["COM1.json", ["Windows reserved name: COM1"]],
    ["report:2026.md", ['forbidden char: ":"']],
    ["post ", ["leading/trailing whitespace", "trailing space or dot"]],
    ["draft.", ["trailing space or dot"]],
    ["bad|name.txt", ['forbidden char: "|"']],
    ["a".repeat(201) + ".md", ["name too long (>200 bytes)"]],
  ];

  let failed = 0;
  for (const [name, expected] of cases) {
    const got = checkFilenameComponent(name);
    const ok =
      got.length === expected.length &&
      expected.every((issue) => got.includes(issue));
    if (!ok) {
      failed += 1;
      console.error(
        `  FAIL ${JSON.stringify(name)} expected ${JSON.stringify(expected)} got ${JSON.stringify(got)}`,
      );
    }
  }
  if (failed) {
    console.error(`\n${failed} self-check assertion(s) failed`);
    process.exit(1);
  }
  console.log(`lint-filenames self-check OK (${cases.length} cases)`);
}

function lintPathsFromHits(hits, label, scanned) {
  console.log(`${label}: scanned ${scanned} path(s)`);
  if (!hits.length) {
    console.log("No cross-platform unsafe filenames found.");
    return 0;
  }
  for (const { path, component, issues } of hits) {
    console.error(`${path}  [${component}]`);
    for (const issue of issues) console.error(`  - ${issue}`);
  }
  console.error(`\n${hits.length} unsafe path component(s)`);
  return 1;
}

function lintPaths(paths, label) {
  const hits = [];
  for (const rel of paths) {
    const parts = rel.replace(/\\/g, "/").split("/");
    for (const part of parts) {
      const issues = checkFilenameComponent(part);
      if (issues.length) hits.push({ path: rel, component: part, issues });
    }
  }
  return lintPathsFromHits(hits, label, paths.length);
}

function main() {
  if (process.argv.includes("--self-check")) {
    runSelfCheck();
    return;
  }

  if (process.argv.includes("--walk")) {
    const hits = [];
    const scanned = walkTree(projectRoot, hits);
    process.exit(lintPathsFromHits(hits, "Working tree", scanned));
  }

  process.exit(lintPaths(gitTrackedFiles(), "Git tracked"));
}

main();
