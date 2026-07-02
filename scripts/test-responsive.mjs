#!/usr/bin/env node
/**
 * Responsive layout regression checks for custom templates and CSS.
 *
 * Usage:
 *   node scripts/test-responsive.mjs
 *   node scripts/test-responsive.mjs --build   # regenerate public/ first
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative } from "node:path";
import { ensureHugo } from "./ensureHugo.mjs";
import { projectRoot, run, runNodeScript } from "./spawnUtil.mjs";

const LAYOUT_ROOTS = [
  join(projectRoot, "layouts"),
  join(projectRoot, "themes/jorap/layouts"),
];
const CSS_FILES = [
  join(projectRoot, "assets/css/custom.css"),
  join(projectRoot, "themes/jorap/assets/css/components.css"),
  join(projectRoot, "themes/jorap/assets/css/navigation.css"),
];
const PAGE_TEMPLATES = [
  "themes/jorap/layouts/home.html",
  "themes/jorap/layouts/blog/single.html",
  "layouts/blog/list.html",
  "layouts/notes/single.html",
  "layouts/notes/list.html",
  "layouts/notes/graph.html",
  "layouts/notes/cards.html",
  "layouts/notes/review.html",
  "layouts/notes/backlinks.html",
  "layouts/notes/issues.html",
  "layouts/notes/create.html",
  "layouts/notes/random-duo.html",
  "layouts/drafts/list.html",
  "themes/jorap/layouts/single.html",
  "themes/jorap/layouts/list.html",
  "themes/jorap/layouts/term.html",
  "themes/jorap/layouts/taxonomy.html",
  "themes/jorap/layouts/about/list.html",
  "themes/jorap/layouts/contact/list.html",
  "themes/jorap/layouts/authors/list.html",
  "themes/jorap/layouts/authors/single.html",
  "themes/jorap/layouts/404.en.html",
];

let failed = 0;

function fail(message) {
  failed += 1;
  console.error(`  FAIL ${message}`);
}

function ok(message) {
  console.log(`  ok ${message}`);
}

function assert(condition, message) {
  if (!condition) fail(message);
  else ok(message);
}

function walkHtml(dir, files = []) {
  if (!existsSync(dir)) return files;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) walkHtml(path, files);
    else if (entry.name.endsWith(".html")) files.push(path);
  }
  return files;
}

function maybeBuild() {
  if (!process.argv.includes("--build")) return;
  const hugoBin = ensureHugo();
  runNodeScript(join(projectRoot, "scripts", "themeGenerator.js"));
  runNodeScript(join(projectRoot, "scripts", "noteFileDates.js"));
  run(hugoBin, ["--gc", "--minify", "--buildFuture"], { cwd: projectRoot });
}

function testLayoutAntiPatterns() {
  console.log("\nlayout anti-patterns");
  const files = LAYOUT_ROOTS.flatMap((root) => walkHtml(root));
  const offenders = [];

  for (const file of files) {
    const rel = relative(projectRoot, file);
    const text = readFileSync(file, "utf8");

    if (/\bmb:[a-z]+-/.test(text) || /\bmt:[a-z]+-/.test(text)) {
      offenders.push(`${rel}: invalid Tailwind variant (use md:mb-0 not mb:md-0)`);
    }
    if (/\b(input-group|form-control|w-75)\b/.test(text)) {
      offenders.push(`${rel}: legacy Bootstrap class without theme equivalent`);
    }
    if (/\bgrid-cols-(?:[5-9]|1[0-2])\b/.test(text) && !/\b(?:sm|md|lg|xl|2xl):grid-cols-/.test(text)) {
      offenders.push(`${rel}: fixed grid-cols-N without responsive breakpoint`);
    }
  }

  assert(offenders.length === 0, offenders.length ? offenders.join("; ") : "no layout anti-patterns");
}

function testPageTemplates() {
  console.log("\npage templates");
  for (const rel of PAGE_TEMPLATES) {
    const path = join(projectRoot, rel);
    assert(existsSync(path), `${rel} exists`);
    if (!existsSync(path)) continue;

    const text = readFileSync(path, "utf8");
    const hasResponsiveShell =
      text.includes("container") ||
      text.includes("max-w-") ||
      text.includes("section");
    assert(hasResponsiveShell, `${rel} uses container/section/max-width shell`);

    const isSidebarLayout =
      rel.includes("single.html") ||
      rel.includes("blog/list") ||
      rel.includes("drafts/list") ||
      rel.includes("term.html");
    if (isSidebarLayout) {
      assert(
        /lg:col-|md:col-|hidden lg:|lg:hidden/.test(text),
        `${rel} stacks sidebars with responsive columns`,
      );
    }
  }
}

function testResponsiveCss() {
  console.log("\nresponsive CSS guards");
  const custom = readFileSync(join(projectRoot, "assets/css/custom.css"), "utf8");
  const components = readFileSync(
    join(projectRoot, "themes/jorap/assets/css/components.css"),
    "utf8",
  );

  assert(
    custom.includes(".notes-random-controls") &&
      custom.includes("grid-template-columns: minmax(0, 1fr) auto"),
    "random note controls use shrink-safe grid layout",
  );
  assert(
    components.includes("prose-pre:overflow-x-auto") &&
      components.includes("prose-table:overflow-x-auto"),
    "prose pre/table horizontal scroll",
  );
  assert(
    custom.includes(".notes-issues__item") && custom.includes("overflow-wrap"),
    "issues list wraps long wikilink codes",
  );
}

function testBuiltHtml() {
  console.log("\nbuilt HTML viewport");
  const home = join(projectRoot, "public", "index.html");
  if (!existsSync(home)) {
    fail("public/index.html missing (run pnpm build or pass --build)");
    return;
  }

  const html = readFileSync(home, "utf8");
  assert(html.includes('name="viewport"'), "homepage sets viewport meta");
  assert(html.includes("width=device-width"), "homepage viewport includes device-width");
  assert(html.includes("search-modal"), "homepage search modal present");
  assert(/data-search-input/.test(html), "homepage search input present");

  const hubPath = join(
    projectRoot,
    "public",
    "notes",
    "pressure-reveals-weakness",
    "index.html",
  );
  if (existsSync(hubPath)) {
    const hub = readFileSync(hubPath, "utf8");
    assert(
      !hub.includes("notes-outgoing border"),
      "hub page with body wikilinks skips duplicate Links from this Note",
    );
  }
}

function main() {
  console.log("test-responsive");
  maybeBuild();

  for (const file of CSS_FILES) {
    assert(existsSync(file), `${relative(projectRoot, file)} exists`);
  }

  testLayoutAntiPatterns();
  testPageTemplates();
  testResponsiveCss();
  testBuiltHtml();

  console.log(`\n${failed === 0 ? "all passed" : `${failed} failed`}`);
  process.exit(failed === 0 ? 0 : 1);
}

main();
