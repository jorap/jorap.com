# TODO — JoRap Notes

Working backlog. Shipped items stay listed for context; open items are what to pick up next.

**Last reviewed:** 2026-07-02

---

## Shipped (reference)

Recent work already live or documented — no action unless regressing:

- Skip-to-content link, nav keyboard nav, theme-switcher a11y
- 44px touch targets and `focus-visible` rings (nav, filters, buttons, footer)
- Semantic warning/error/success/graph tokens (`data/theme.json`)
- Notes graph (PixiJS), flashcards, expanded list filters, backlinks panel
- `prefers-reduced-motion` on flashcards, scroll, progress ring
- Security headers + build-time CSP hashes (`static/_headers`, `cspHashes.mjs`)
- Self-hosted Inter with `font-display: swap`
- Related posts on blog and notes
- Breadcrumbs on page headers
- Back-to-top control with progress ring
- Apex → www redirects (`static/_redirects`)
- Design system docs (`docs/DESIGN.md`, `docs/DESIGN.json`, `.impeccable/design.json`)
- `[skip ci]` git hook for non-deploy commits

---

## Open — high value

- [ ] **Critical CSS / above-the-fold CSS** — inline or early-load key shell styles to improve FCP on slow networks
- [ ] **Core Web Vitals pass** — run PageSpeed on home, blog post, notes list; fix any LCP/CLS regressions
- [ ] **Image audit** — WebP/AVIF where missing; explicit dimensions on content images to prevent CLS
- [ ] **Privacy policy refresh** — align with GTM, Cloudflare Web Analytics, Disqus embeds actually in use

---

## Open — medium

- [ ] **Reading progress bar** on long blog posts (optional; must respect reduced motion)
- [ ] **Archive by date** page for blog (if SEO/discovery warrants it)
- [ ] **Newsletter signup** — only if there is a sending workflow behind it
- [ ] **Structured data audit** — Article/Person/BreadcrumbList JSON-LD consistency
- [ ] **ESLint for `assets/js`** — catch regressions in graph/flashcard modules

---

## Open — low / exploratory

- [ ] **Service worker / offline** — PWA module exists upstream; evaluate cost vs benefit on Cloudflare free tier
- [ ] **Design direction prototype** — pick one page to try an alternative from `DESIGN.md` (institutional, typographic, committed color)
- [ ] **Component extraction** — only if a third surface repeats the same markup; avoid premature abstraction

---

## Not pursuing (by design)

- Generic SaaS landing patterns (hero metrics, three-icon rows)
- Second brand accent color or display font without explicit PRODUCT.md change
- Performative dev-bro chrome on the marketing shell

---

*Review monthly. Move shipped items down; delete ideas that aged out.*
