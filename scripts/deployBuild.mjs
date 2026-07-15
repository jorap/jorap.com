#!/usr/bin/env node
/**
 * Canonical production build for local CI and all deployment targets.
 * Runs theme generation, note dates, Hugo, and CSP hashing — never bare `hugo`.
 */
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { ensureHugo } from "./ensureHugo.mjs";
import { projectRoot, run, runNodeScript } from "./spawnUtil.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

process.env.HUGO_ENV ||= "production";
process.env.NODE_ENV ||= "production";

require("./fix-tailwind-bin.js");

const hugoBin = ensureHugo();

runNodeScript(join(__dirname, "themeGenerator.js"));
runNodeScript(join(__dirname, "noteFileDates.js"));
run("python3", [join(__dirname, "export-okf-bundle.py")], { cwd: projectRoot });
run("python3", [join(__dirname, "export-okf-blog-bundle.py")], { cwd: projectRoot });
const hugoCacheDir = join(projectRoot, ".cache");
run(
  hugoBin,
  [
    "--gc",
    "--minify",
    "--forceSyncStatic",
    "--buildFuture",
    "--cacheDir",
    hugoCacheDir,
  ],
  { cwd: projectRoot },
);
runNodeScript(join(__dirname, "cspHashes.mjs"));
