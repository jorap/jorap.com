#!/usr/bin/env node
/**
 * Verify Cursor and Kilo Code share one agent config tree (.cursor/).
 *
 * Usage:
 *   node scripts/lint-agent-config.mjs
 *   node scripts/lint-agent-config.mjs --self-check
 */
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { projectRoot } from "./spawnUtil.mjs";

const CANONICAL_SKILLS = ".cursor/skills";
const CANONICAL_RULES_GLOB = ".cursor/rules/*.mdc";
const KILO_CONFIG = "kilo.jsonc";
const AGENTS_MD = "AGENTS.md";

const FORBIDDEN_DUPLICATE_DIRS = [
  ".kilo/skills",
  ".kilo/rules",
  ".kilocode/skills",
  ".kilocode/rules",
  ".agents/skills",
];

/** Strip line and block comments so JSON.parse accepts kilo.jsonc. */
export function parseJsonc(text) {
  let out = "";
  let i = 0;
  while (i < text.length) {
    if (text[i] === '"') {
      out += text[i++];
      while (i < text.length) {
        out += text[i];
        if (text[i] === "\\") {
          i += 1;
          if (i < text.length) out += text[i];
        } else if (text[i] === '"') {
          i += 1;
          break;
        }
        i += 1;
      }
      continue;
    }
    if (text.startsWith("//", i)) {
      i = text.indexOf("\n", i);
      if (i === -1) break;
      continue;
    }
    if (text.startsWith("/*", i)) {
      const end = text.indexOf("*/", i + 2);
      if (end === -1) throw new Error("unclosed block comment in JSONC");
      i = end + 2;
      continue;
    }
    out += text[i++];
  }
  return JSON.parse(out);
}

/** @returns {{ frontmatter: Record<string, string>, body: string } | null} */
export function parseFrontmatter(text) {
  if (!text.startsWith("---\n")) return null;
  const end = text.indexOf("\n---\n", 4);
  if (end === -1) return null;
  const block = text.slice(4, end);
  /** @type {Record<string, string>} */
  const frontmatter = {};
  for (const line of block.split("\n")) {
    const m = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    frontmatter[m[1]] = m[2].trim();
  }
  return { frontmatter, body: text.slice(end + 5) };
}

/** @returns {string[]} */
export function listSkillDirs(skillsRoot) {
  const abs = join(projectRoot, skillsRoot);
  if (!existsSync(abs)) return [];
  return readdirSync(abs, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();
}

/** @returns {string[]} */
export function listRuleFiles(rulesRoot) {
  const abs = join(projectRoot, rulesRoot);
  if (!existsSync(abs)) return [];
  return readdirSync(abs)
    .filter((f) => f.endsWith(".mdc"))
    .sort();
}

/** @returns {{ errors: string[], warnings: string[] }} */
export function lintAgentConfig(root = projectRoot) {
  const errors = [];
  const warnings = [];

  const kiloPath = join(root, KILO_CONFIG);
  if (!existsSync(kiloPath)) {
    errors.push(`missing ${KILO_CONFIG}`);
    return { errors, warnings };
  }

  let kilo;
  try {
    kilo = parseJsonc(readFileSync(kiloPath, "utf8"));
  } catch (e) {
    errors.push(`${KILO_CONFIG}: ${e.message}`);
    return { errors, warnings };
  }

  const skillPaths = kilo?.skills?.paths;
  if (!Array.isArray(skillPaths) || skillPaths.length !== 1) {
    errors.push(
      `${KILO_CONFIG}: skills.paths must be exactly [".cursor/skills"]`,
    );
  } else if (skillPaths[0] !== CANONICAL_SKILLS) {
    errors.push(
      `${KILO_CONFIG}: skills.paths[0] must be ".cursor/skills", got ${JSON.stringify(skillPaths[0])}`,
    );
  }

  const instructions = kilo?.instructions;
  if (!Array.isArray(instructions)) {
    errors.push(`${KILO_CONFIG}: instructions must be an array`);
  } else {
    if (!instructions.includes(AGENTS_MD)) {
      errors.push(`${KILO_CONFIG}: instructions must include "AGENTS.md"`);
    }
    if (!instructions.includes(CANONICAL_RULES_GLOB)) {
      errors.push(
        `${KILO_CONFIG}: instructions must include ".cursor/rules/*.mdc"`,
      );
    }
    for (const entry of instructions) {
      if (
        typeof entry === "string" &&
        (entry.includes(".kilo/") ||
          entry.includes(".kilocode/") ||
          entry.includes(".agents/skills"))
      ) {
        errors.push(
          `${KILO_CONFIG}: instructions must not point at duplicate trees: ${entry}`,
        );
      }
    }
  }

  const agentsPath = join(root, AGENTS_MD);
  if (!existsSync(agentsPath)) {
    errors.push(`missing ${AGENTS_MD}`);
  } else {
    const agents = readFileSync(agentsPath, "utf8");
    if (!agents.includes(".cursor/rules/")) {
      errors.push(`${AGENTS_MD}: must reference .cursor/rules/`);
    }
    if (!agents.includes(".cursor/skills/")) {
      errors.push(`${AGENTS_MD}: must reference .cursor/skills/`);
    }
    if (!agents.includes("lint:agent-config")) {
      errors.push(`${AGENTS_MD}: must mention pnpm lint:agent-config`);
    }
  }

  for (const rel of FORBIDDEN_DUPLICATE_DIRS) {
    const abs = join(root, rel);
    if (!existsSync(abs)) continue;
    const st = statSync(abs);
    if (st.isDirectory()) {
      const entries = readdirSync(abs);
      if (entries.length > 0) {
        errors.push(
          `forbidden duplicate tree ${rel}/ (${entries.length} entries) — use ${CANONICAL_SKILLS} or .cursor/rules/ only`,
        );
      }
    } else {
      errors.push(`forbidden duplicate path ${rel} (not a directory)`);
    }
  }

  for (const name of listSkillDirs(CANONICAL_SKILLS)) {
    const skillMd = join(root, CANONICAL_SKILLS, name, "SKILL.md");
    if (!existsSync(skillMd)) {
      errors.push(`${CANONICAL_SKILLS}/${name}/: missing SKILL.md`);
      continue;
    }
    const parsed = parseFrontmatter(readFileSync(skillMd, "utf8"));
    if (!parsed) {
      errors.push(`${CANONICAL_SKILLS}/${name}/SKILL.md: missing YAML frontmatter`);
      continue;
    }
    if (!parsed.frontmatter.description) {
      errors.push(`${CANONICAL_SKILLS}/${name}/SKILL.md: missing description`);
    }
    if (parsed.frontmatter.name && parsed.frontmatter.name !== name) {
      errors.push(
        `${CANONICAL_SKILLS}/${name}/SKILL.md: name "${parsed.frontmatter.name}" must match directory`,
      );
    }
  }

  for (const file of listRuleFiles(".cursor/rules")) {
    const rel = `.cursor/rules/${file}`;
    const parsed = parseFrontmatter(readFileSync(join(root, rel), "utf8"));
    if (!parsed) {
      errors.push(`${rel}: missing YAML frontmatter`);
      continue;
    }
    if (!parsed.frontmatter.description) {
      errors.push(`${rel}: missing description in frontmatter`);
    }
  }

  return { errors, warnings };
}

function runSelfCheck() {
  const jsonc = `{
  // comment
  "skills": { "paths": [".cursor/skills"] },
  "instructions": ["AGENTS.md", ".cursor/rules/*.mdc"]
}`;
  const parsed = parseJsonc(jsonc);
  if (parsed.skills.paths[0] !== ".cursor/skills") {
    console.error("parseJsonc self-check failed");
    process.exit(1);
  }

  const fm = parseFrontmatter('---\ndescription: test\nalwaysApply: true\n---\n# Body\n');
  if (!fm || fm.frontmatter.description !== "test") {
    console.error("parseFrontmatter self-check failed");
    process.exit(1);
  }

  console.log("lint-agent-config self-check OK");
}

function main() {
  if (process.argv.includes("--self-check")) {
    runSelfCheck();
    return;
  }

  const { errors } = lintAgentConfig();
  if (!errors.length) {
    const skills = listSkillDirs(CANONICAL_SKILLS).length;
    const rules = listRuleFiles(".cursor/rules").length;
    console.log(
      `agent config OK: ${skills} skill(s), ${rules} rule(s), Kilo → ${CANONICAL_SKILLS}`,
    );
    return;
  }

  for (const err of errors) console.error(`  - ${err}`);
  console.error(`\n${errors.length} agent config issue(s)`);
  process.exit(1);
}

main();
