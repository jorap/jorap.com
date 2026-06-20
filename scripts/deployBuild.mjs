#!/usr/bin/env node
/**
 * Canonical production build for local CI and all deployment targets.
 * Runs theme generation, note dates, Hugo, and CSP hashing — never bare `hugo`.
 */
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  capture,
  projectRoot,
  run,
  runNodeScript,
} from "./spawnUtil.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

process.env.HUGO_ENV ||= "production";
process.env.NODE_ENV ||= "production";

require("./fix-tailwind-bin.js");

const pinnedHugo = JSON.parse(
  readFileSync(join(__dirname, "deploy-versions.json"), "utf8"),
).hugo;

function assertHugoVersion() {
  const result = capture("hugo", ["version"]);
  if (result.status !== 0 || !result.stdout) {
    console.error("[deploy] hugo is not installed or not on PATH.");
    process.exit(1);
  }

  const versionLine = result.stdout.trim();
  if (!/extended/i.test(versionLine)) {
    console.error("[deploy] Hugo Extended is required (css.TailwindCSS).");
    console.error(`[deploy] Got: ${versionLine}`);
    process.exit(1);
  }

  const match = versionLine.match(/v(\d+\.\d+\.\d+)/);
  if (match && match[1] !== pinnedHugo) {
    console.warn(
      `[deploy] Hugo ${match[1]} != pinned ${pinnedHugo}. Set HUGO_VERSION=${pinnedHugo} in CI.`,
    );
  }
}

assertHugoVersion();

runNodeScript(join(__dirname, "themeGenerator.js"));
runNodeScript(join(__dirname, "noteFileDates.js"));
run("hugo", ["--gc", "--minify", "--forceSyncStatic"], { cwd: projectRoot });
runNodeScript(join(__dirname, "cspHashes.mjs"));
