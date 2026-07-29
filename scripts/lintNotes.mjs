#!/usr/bin/env node
/** Wikilink lint via Hugo build output (no shell rg pipe). */
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { capture, runNodeScript } from "./spawnUtil.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const WIKILINK_RE = /broken wikilink|unlinked mention/;

runNodeScript(join(__dirname, "themeGenerator.js"));
runNodeScript(join(__dirname, "noteFileDates.js"));

const hugo = capture("hugo", ["--gc"]);
const output = `${hugo.stdout || ""}${hugo.stderr || ""}`;
for (const line of output.split("\n")) {
  if (WIKILINK_RE.test(line)) console.log(line);
}

// ponytail: report-only lint (original shell used `|| true`)
process.exit(0);
