#!/usr/bin/env node
import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const BASE = process.argv[2] || "http://localhost:1313";
const OUT = path.join(process.cwd(), "tmp/responsive-screenshots");

const checks = [
  { vp: "mobile", width: 390, height: 844 },
  { vp: "tablet", width: 768, height: 1024 },
];

const pages = ["/", "/blog/", "/notes/", "/about/", "/blog/how-i-built-jorap-notes/"];

fs.mkdirSync(OUT, { recursive: true });

async function layoutCheck(page, width, height, urlPath) {
  await page.setViewportSize({ width, height });
  await page.goto(`${BASE}${urlPath}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(500);

  return page.evaluate(() => {
    const vw = window.innerWidth;
    const overflow = document.documentElement.scrollWidth - vw;

    const header = document.querySelector("header");
    const navMenu = document.querySelector("#nav-menu");
    const navToggleLabel = document.querySelector('label[for="nav-toggle"]');
    const hero = document.querySelector("main h1, .banner h1, section h1");
    const gridCols = [...document.querySelectorAll("[class*='col-']")].slice(0, 3).map((el) => ({
      cls: el.className.split(" ").filter((c) => c.startsWith("col") || c.startsWith("md:") || c.startsWith("lg:")).join(" "),
      width: Math.round(el.getBoundingClientRect().width),
    }));

    const blogCards = [...document.querySelectorAll(".blog-card, article")].slice(0, 2).map((el) => ({
      width: Math.round(el.getBoundingClientRect().width),
      fits: el.getBoundingClientRect().width <= vw,
    }));

    const navComputed = navMenu ? getComputedStyle(navMenu) : null;
    const navRect = navMenu?.getBoundingClientRect();

    return {
      title: document.title.slice(0, 60),
      overflow,
      headerHeight: header ? Math.round(header.getBoundingClientRect().height) : null,
      navMenuDisplay: navComputed?.display,
      navMenuVisible: navRect ? navRect.width > 0 && navRect.height > 0 : false,
      navToggleSize: navToggleLabel
        ? {
            w: Math.round(navToggleLabel.getBoundingClientRect().width),
            h: Math.round(navToggleLabel.getBoundingClientRect().height),
          }
        : null,
      heroFontSize: hero ? getComputedStyle(hero).fontSize : null,
      heroWidth: hero ? Math.round(hero.getBoundingClientRect().width) : null,
      gridCols,
      blogCards,
      bodyFontSize: getComputedStyle(document.body).fontSize,
    };
  });
}

async function testNav(page) {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });

  const before = await page.evaluate(() => {
    const m = document.querySelector("#nav-menu");
    return m ? getComputedStyle(m).display : null;
  });

  await page.locator('label[for="nav-toggle"]').click();
  await page.waitForTimeout(200);

  const after = await page.evaluate(() => {
    const m = document.querySelector("#nav-menu");
    const rect = m?.getBoundingClientRect();
    return {
      display: m ? getComputedStyle(m).display : null,
      height: rect ? Math.round(rect.height) : 0,
      linkCount: m ? m.querySelectorAll("a.nav-link, .nav-link").length : 0,
    };
  });

  return { before, after, opens: after.display === "block" && after.height > 50 };
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log("\nLayout metrics\n" + "=".repeat(50));

  for (const c of checks) {
    console.log(`\n### ${c.vp} (${c.width}×${c.height})`);
    for (const p of pages) {
      const m = await layoutCheck(page, c.width, c.height, p);
      const status = m.overflow > 1 ? "OVERFLOW" : "OK";
      console.log(`  [${status}] ${p}`);
      console.log(`       overflow: ${m.overflow}px | header: ${m.headerHeight}px | body font: ${m.bodyFontSize}`);
      console.log(`       nav visible: ${m.navMenuVisible} (${m.navMenuDisplay}) | toggle: ${JSON.stringify(m.navToggleSize)}`);
      if (m.heroFontSize) console.log(`       hero: ${m.heroFontSize} / ${m.heroWidth}px wide`);
      if (m.blogCards.length) console.log(`       cards: ${JSON.stringify(m.blogCards)}`);
    }
  }

  const nav = await testNav(page);
  console.log(`\n### Mobile nav toggle`);
  console.log(`  before: ${nav.before} → after: ${nav.after.display} (h=${nav.after.height}, links=${nav.after.linkCount})`);
  console.log(`  [${nav.opens ? "OK" : "FAIL"}] Menu ${nav.opens ? "opens" : "does not open"}`);

  // Viewport screenshots (above-the-fold)
  for (const c of checks) {
    await page.setViewportSize({ width: c.width, height: c.height });
    await page.goto(`${BASE}/`, { waitUntil: "networkidle" });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, `${c.vp}__home-fold.png`) });

    await page.locator('label[for="nav-toggle"]').click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(OUT, `${c.vp}__home-nav-open-fold.png`) });
    // reset
    await page.locator('label[for="nav-toggle"]').click();
  }

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${BASE}/blog/`, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(OUT, "mobile__blog-fold.png") });

  await browser.close();
  console.log(`\nViewport screenshots saved to ${OUT}\n`);
}

main();
