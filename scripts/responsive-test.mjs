#!/usr/bin/env node
/**
 * Responsive layout audit for mobile + tablet viewports.
 * Usage: node scripts/responsive-test.mjs [baseURL]
 */

import { chromium, devices } from "playwright";

const BASE = process.argv[2] || "http://localhost:1313";

const VIEWPORTS = [
  { name: "mobile", width: 390, height: 844, label: "iPhone 14" },
  { name: "mobile-sm", width: 320, height: 568, label: "iPhone SE" },
  { name: "tablet", width: 768, height: 1024, label: "iPad portrait" },
  { name: "tablet-land", width: 1024, height: 768, label: "iPad landscape" },
];

const PAGES = [
  { path: "/", name: "Home" },
  { path: "/about/", name: "About" },
  { path: "/blog/", name: "Blog" },
  { path: "/notes/", name: "Notes" },
  { path: "/contact/", name: "Contact" },
  { path: "/blog/how-i-built-jorap-notes/", name: "Blog post" },
];

async function auditPage(page, viewport, pageInfo) {
  const url = `${BASE}${pageInfo.path}`;
  const issues = [];

  await page.setViewportSize({ width: viewport.width, height: viewport.height });
  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });

  const metrics = await page.evaluate(() => {
    const vw = window.innerWidth;
    const docW = document.documentElement.scrollWidth;
    const bodyW = document.body.scrollWidth;
    const overflow = Math.max(docW, bodyW) - vw;

    const offenders = [];
    const walk = (el) => {
      const rect = el.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) return;
      const right = rect.right + window.scrollX;
      if (right > vw + 2) {
        const tag = el.tagName.toLowerCase();
        const cls =
          typeof el.className === "string" && el.className
            ? `.${el.className.trim().split(/\s+/).slice(0, 3).join(".")}`
            : "";
        offenders.push({
          tag,
          cls: cls.slice(0, 80),
          overflowPx: Math.round(right - vw),
          width: Math.round(rect.width),
        });
      }
      for (const child of el.children) walk(child);
    };
    walk(document.body);

    offenders.sort((a, b) => b.overflowPx - a.overflowPx);
    const unique = [];
    const seen = new Set();
    for (const o of offenders) {
      const key = `${o.tag}${o.cls}`;
      if (seen.has(key)) continue;
      seen.add(key);
      unique.push(o);
      if (unique.length >= 5) break;
    }

    const smallTargets = [];
    const interactive = document.querySelectorAll(
      "a, button, input, select, textarea, [role='button'], summary"
    );
    for (const el of interactive) {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) continue;
      if (rect.width < 44 || rect.height < 44) {
        const text = (el.textContent || el.getAttribute("aria-label") || "")
          .trim()
          .slice(0, 40);
        if (!text && el.tagName !== "INPUT") continue;
        smallTargets.push({
          tag: el.tagName.toLowerCase(),
          text,
          w: Math.round(rect.width),
          h: Math.round(rect.height),
        });
        if (smallTargets.length >= 5) break;
      }
    }

    const navToggle = document.querySelector(
      "#nav-toggle, .nav-toggle, [data-nav-toggle], button[aria-controls*='nav'], .hamburger"
    );
    const navMenu = document.querySelector(
      "#nav-menu, .nav-menu, nav ul, .navbar-nav"
    );

    return {
      overflow,
      offenders: unique,
      smallTargets,
      hasNavToggle: !!navToggle,
      navToggleVisible: navToggle
        ? navToggle.getBoundingClientRect().width > 0
        : false,
      navMenuHidden: navMenu
        ? getComputedStyle(navMenu).display === "none" ||
          navMenu.getBoundingClientRect().width === 0
        : null,
      title: document.title,
    };
  });

  if (metrics.overflow > 1) {
    issues.push({
      type: "horizontal-overflow",
      severity: "error",
      detail: `${Math.round(metrics.overflow)}px wider than viewport`,
      offenders: metrics.offenders,
    });
  }

  if (viewport.width <= 768 && !metrics.hasNavToggle) {
    issues.push({
      type: "missing-mobile-nav",
      severity: "warn",
      detail: "No hamburger / nav toggle detected on small screen",
    });
  }

  if (viewport.width <= 768 && metrics.smallTargets.length > 0) {
    issues.push({
      type: "small-touch-targets",
      severity: "warn",
      detail: `${metrics.smallTargets.length}+ interactive elements under 44×44px`,
      targets: metrics.smallTargets,
    });
  }

  return { url, metrics, issues };
}

async function testMobileNav(page) {
  const url = `${BASE}/`;
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(url, { waitUntil: "networkidle" });

  const toggleSelectors = [
    "#nav-toggle",
    ".nav-toggle",
    "[data-nav-toggle]",
    "button[aria-label*='menu' i]",
    "button[aria-label*='Menu' i]",
    ".navbar-toggler",
    "label[for='nav-toggle']",
    "label[for='menu-toggle']",
    "#menu-toggle",
  ];

  let toggle = null;
  for (const sel of toggleSelectors) {
    const el = page.locator(sel).first();
    if ((await el.count()) > 0 && (await el.isVisible())) {
      toggle = el;
      break;
    }
  }

  if (!toggle) {
    return { works: false, detail: "No visible nav toggle found" };
  }

  await toggle.click();
  await page.waitForTimeout(400);

  const menuVisible = await page.evaluate(() => {
    const menus = document.querySelectorAll(
      "nav ul, .nav-menu, #nav-menu, .navbar-nav, [data-nav-menu]"
    );
    for (const menu of menus) {
      const style = getComputedStyle(menu);
      const rect = menu.getBoundingClientRect();
      if (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        style.opacity !== "0" &&
        rect.height > 20 &&
        rect.width > 50
      ) {
        return true;
      }
    }
    const open = document.querySelector(
      ".nav-open nav, .menu-open nav, nav.open, .navbar-collapse.show, input#nav-toggle:checked ~ nav, input#menu-toggle:checked ~ nav"
    );
    return !!open;
  });

  return {
    works: menuVisible,
    detail: menuVisible ? "Menu opens on tap" : "Toggle clicked but menu not visible",
  };
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const results = [];
  let errorCount = 0;
  let warnCount = 0;

  console.log(`\nResponsive audit — ${BASE}\n${"=".repeat(60)}\n`);

  for (const vp of VIEWPORTS) {
    console.log(`\n## ${vp.label} (${vp.width}×${vp.height})\n`);
    for (const pg of PAGES) {
      try {
        const result = await auditPage(page, vp, pg);
        results.push({ viewport: vp.name, ...result });

        const errors = result.issues.filter((i) => i.severity === "error");
        const warns = result.issues.filter((i) => i.severity === "warn");
        errorCount += errors.length;
        warnCount += warns.length;

        const status =
          errors.length > 0 ? "FAIL" : warns.length > 0 ? "WARN" : "OK";
        console.log(`  [${status}] ${pg.name} (${pg.path})`);

        for (const issue of result.issues) {
          console.log(`       ${issue.severity.toUpperCase()}: ${issue.type} — ${issue.detail}`);
          if (issue.offenders?.length) {
            for (const o of issue.offenders) {
              console.log(`         → <${o.tag}${o.cls}> +${o.overflowPx}px (w=${o.width})`);
            }
          }
          if (issue.targets?.length) {
            for (const t of issue.targets.slice(0, 3)) {
              console.log(`         → <${t.tag}> "${t.text}" ${t.w}×${t.h}px`);
            }
          }
        }
      } catch (err) {
        console.log(`  [ERROR] ${pg.name} — ${err.message}`);
        errorCount++;
      }
    }
  }

  console.log(`\n## Mobile navigation\n`);
  try {
    const nav = await testMobileNav(page);
    console.log(`  [${nav.works ? "OK" : "FAIL"}] ${nav.detail}`);
    if (!nav.works) errorCount++;
  } catch (err) {
    console.log(`  [ERROR] ${err.message}`);
    errorCount++;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(`Summary: ${errorCount} error(s), ${warnCount} warning(s)`);
  console.log(`${"=".repeat(60)}\n`);

  await browser.close();
  process.exit(errorCount > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
