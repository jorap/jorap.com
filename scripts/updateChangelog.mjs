#!/usr/bin/env node
/**
 * Append functional file changes to CHANGELOG.md (today's date section).
 * Invoked from the prepare-commit-msg git hook; skips content and agent paths.
 */
import fs from "node:fs";
import path from "node:path";
import { capture, projectRoot } from "./spawnUtil.mjs";

const CHANGELOG = path.join(projectRoot, "CHANGELOG.md");
const TODAY = new Date().toISOString().slice(0, 10);

/** @returns {boolean} */
function isFunctional(file) {
  if (!file) return false;
  if (/^content\//.test(file)) return false;
  if (/^\.specstory\//.test(file)) return false;
  if (/^\.cursor\//.test(file)) return false;
  if (/^\.agents\//.test(file)) return false;
  if (/^exports\//.test(file)) return false;
  if (/^public\//.test(file)) return false;
  if (/^data\/noteFileDates\.json$/.test(file)) return false;
  if (/^CHANGELOG\.md$/.test(file)) return false;
  if (/^README\.md$/.test(file)) return false;
  if (/^docs\//.test(file)) return false;
  if (/^static\//.test(file) && !/^static\/(_headers|_redirects)/.test(file)) {
    return false;
  }
  if (/\.md$/.test(file)) return false;

  if (
    /^(layouts|assets\/js|assets\/css|themes|scripts|config|functions)\//.test(
      file,
    )
  ) {
    return true;
  }
  if (file === "data/theme.json") return true;
  if (/^(wrangler|netlify|hugo)\.toml$/.test(file)) return true;
  if (file === ".gitlab-ci.yml") return true;
  if (file === "package.json" || file === "pnpm-lock.yaml") return true;
  if (/^static\/(_headers|_redirects)/.test(file)) return true;
  return false;
}

/** @param {string} msg */
function categoryFromMessage(msg) {
  const first = msg.trim().split("\n").find((line) => line.trim()) ?? "";
  const head = first.toLowerCase();
  if (/^fix(es)?(\(|:|$|\s)/.test(head)) return "Fixed";
  if (/^(feat|add)(\(|\:|$|\s)/.test(head)) return "Added";
  return "Changed";
}

/** @param {string} content @param {string} date */
function sliceDateSection(content, date) {
  const header = `## ${date}`;
  const start = content.indexOf(header);
  if (start === -1) return null;
  const after = content.indexOf("\n", start) + 1;
  const next = content.indexOf("\n## ", after);
  const end = next === -1 ? content.length : next;
  return { start, end, body: content.slice(after, end) };
}

/** @param {string} body @param {string} category @param {string[]} bullets */
function appendCategory(body, category, bullets) {
  const catHeader = `### ${category}`;
  const catIdx = body.indexOf(catHeader);

  const existing = new Set(
    body
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.startsWith("- ")),
  );
  const fresh = bullets.filter((b) => !existing.has(b.trim()));
  if (!fresh.length) return { body, added: 0 };

  if (catIdx === -1) {
    const block = `${catHeader}\n\n${fresh.join("\n")}\n`;
    const trimmed = body.trimEnd();
    return { body: trimmed ? `${trimmed}\n\n${block}` : block, added: fresh.length };
  }

  const afterCat = catIdx + catHeader.length;
  let sectionEnd = body.indexOf("\n### ", afterCat);
  if (sectionEnd === -1) sectionEnd = body.indexOf("\n---", afterCat);
  if (sectionEnd === -1) sectionEnd = body.length;

  const before = body.slice(0, sectionEnd).trimEnd();
  const after = body.slice(sectionEnd);
  const updated = `${before}\n${fresh.join("\n")}\n${after}`;
  return { body: updated, added: fresh.length };
}

/** @param {string} body */
function trimSectionBody(body) {
  return body.replace(/\n---\s*$/, "").trimEnd();
}

/** @param {string} content @param {string} date @param {string} category @param {string[]} bullets */
function upsert(content, date, category, bullets) {
  const section = sliceDateSection(content, date);
  if (section) {
    const trimmedBody = trimSectionBody(section.body);
    const { body, added } = appendCategory(trimmedBody, category, bullets);
    if (!added) return { content, added: 0 };
    const next =
      content.slice(0, section.start) +
      `## ${date}\n` +
      body +
      "\n\n---\n" +
      content.slice(section.end);
    return { content: next, added };
  }

  const block = [
    `## ${date}`,
    "",
    `### ${category}`,
    "",
    ...bullets,
    "",
    "---",
    "",
  ].join("\n");

  const marker = "\n---\n";
  const idx = content.indexOf(marker);
  if (idx === -1) {
    return { content: content.trimEnd() + "\n\n" + block, added: bullets.length };
  }
  const insertAt = idx + marker.length;
  const next =
    content.slice(0, insertAt) + block + content.slice(insertAt);
  return { content: next, added: bullets.length };
}

const msgPath = process.argv[2];
let commitMsg = "";
if (msgPath && fs.existsSync(msgPath)) {
  commitMsg = fs.readFileSync(msgPath, "utf8");
}

const staged = capture("git", ["diff", "--cached", "--name-only"]);
if (staged.status !== 0) process.exit(0);

const files = staged.stdout
  .trim()
  .split("\n")
  .filter((f) => isFunctional(f));
if (!files.length) process.exit(0);

const category = categoryFromMessage(commitMsg);
const bullets = files.map((f) => `- \`${f}\``);

if (!fs.existsSync(CHANGELOG)) {
  console.error("updateChangelog: CHANGELOG.md not found");
  process.exit(1);
}

const original = fs.readFileSync(CHANGELOG, "utf8");
const { content, added } = upsert(original, TODAY, category, bullets);
if (!added) process.exit(0);

fs.writeFileSync(CHANGELOG, content);
console.log(`changelog: +${added} under ${TODAY} (${category})`);
