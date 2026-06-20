#!/usr/bin/env python3
"""Wire up Obsidian-style wikilinks, aliases, and See also sections across all notes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SKIP_FILES = {"_index.md", "graph.md"}

SEE_ALSO_HEADING = "## See also"
MOC_HEADING = "## Maps"
MIN_BODY_LINKS = 3
MIN_OUTGOING_LINKS = 3


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    fm = text[: end + 4]
    body = text[end + 4 :].lstrip("\n")
    inner = text[3:end].strip()
    return fm, inner, body


def parse_yaml_list(block: str, key: str) -> list[str]:
    match = re.search(rf"^{key}:\s*\[(.*)\]\s*$", block, re.M)
    if not match:
        return []
    return [item.strip().strip('"') for item in match.group(1).split(",") if item.strip()]


def parse_scalar(block: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', block, re.M)
    return match.group(1).strip() if match else ""


def yaml_list(values: list[str]) -> str:
    if not values:
        return "aliases: []"
    quoted = ", ".join(f'"{v}"' for v in values)
    return f"aliases: [{quoted}]"


def suggested_aliases(title: str, slug: str, existing: list[str]) -> list[str]:
    aliases = list(existing)
    seen = {a.lower() for a in aliases}

    def add(value: str) -> None:
        value = value.strip()
        if not value or value.lower() in seen or value.lower() == title.lower():
            return
        aliases.append(value)
        seen.add(value.lower())

    add(slug.replace("-", " "))
    paren = re.search(r"\(([^)]+)\)\s*$", title)
    if paren:
        add(paren.group(1).strip())

    manual: dict[str, list[str]] = {
        "PKM": ["Personal Knowledge Management"],
        "PARA Method": ["PARA"],
        "Maps of Content": ["MOC"],
        "Building a Second Brain": ["Second Brain"],
        "The Second Brain Workflow": ["Second Brain Workflow"],
        "Second Brain Daily Workflow": ["Daily Workflow"],
        "Spaced Repetition Systems (SRS)": ["SRS"],
        "Evergreen vs Fleeting Notes": ["Evergreen vs Fleeting"],
        "Local-first Software": ["Local First"],
        "Note-Taking for Researchers": ["Research Notes"],
        "The Collector's Fallacy": ["Collector's Fallacy"],
        "The 12 Week Year": ["12 Week Year"],
        "The Feynman Technique": ["Feynman Technique"],
        "The Archive Method": ["Archive Method"],
        "The Trusted Inbox": ["Trusted Inbox"],
        "The Garage Concept": ["Garage Concept"],
        "The Future of PKM": ["Future of PKM"],
        "The Knowledge Lifecycle": ["Knowledge Lifecycle"],
        "The Power of Interconnectivity": ["Interconnectivity"],
        "Atomic Design for Notes": ["Atomic Design"],
        "GTD vs PARA": ["GTD"],
        "E2EE Security": ["E2EE"],
        "Privacy and Data Sovereignty": ["Data Sovereignty"],
        "There Is No Perfect Solution": ["No Perfect Solution"],
        "Process Over Outcomes": ["Process Over Outcome"],
        "Anti-Fragile Systems": ["Antifragile"],
    }
    for value in manual.get(title, []):
        add(value)

    if title.endswith(" Method"):
        add(title[: -len(" Method")])
    if title.startswith("The "):
        add(title[4:])

    return aliases


def tag_relatedness(tags_a: list[str], tags_b: list[str]) -> float:
    a, b = set(tags_a), set(tags_b)
    if not a or not b:
        return 0.0
    overlap = len(a & b)
    if overlap == 0:
        return 0.0
    return overlap / min(len(a), len(b))


def existing_wikilinks(body: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"\[\[([^\]|#]+)(?:#[^\]|]+)?\]\]", body)}


def protect_regions(body: str) -> tuple[str, list[tuple[str, str]]]:
    replacements: list[tuple[str, str]] = []
    counter = 0

    def shield(match: re.Match[str]) -> str:
        nonlocal counter
        token = f"@@PROTECT{counter}@@"
        replacements.append((token, match.group(0)))
        counter += 1
        return token

    patterns = [
        r"```[\s\S]*?```",
        r"`[^`\n]+`",
        r"\[\[[^\]]+\]\]",
        r"\[[^\]]+\]\([^)]+\)",
    ]
    protected = body
    for pattern in patterns:
        protected = re.sub(pattern, shield, protected)
    return protected, replacements


def restore_regions(text: str, replacements: list[tuple[str, str]]) -> str:
    for token, original in reversed(replacements):
        text = text.replace(token, original)
    return text


def should_link_target(target: str, title: str) -> bool:
    if " " in target:
        return True
    return target == title or target.isupper() or (len(target) > 3 and target[0].isupper())


def inline_link(body: str, targets: list[tuple[str, str]]) -> str:
    protected, replacements = protect_regions(body)
    for target, title in sorted(targets, key=lambda item: len(item[0]), reverse=True):
        if not target or target in protected or not should_link_target(target, title):
            continue
        pattern = re.compile(rf"(?<!\[)\b{re.escape(target)}\b")
        protected = pattern.sub(f"[[{title}]]", protected, count=3)
    return restore_regions(protected, replacements)


def related_notes(
    stem: str,
    title: str,
    tags: list[str],
    catalog: list[dict],
    limit: int = 5,
) -> list[dict]:
    scored: list[tuple[float, dict]] = []
    for note in catalog:
        if note["stem"] == stem:
            continue
        score = tag_relatedness(tags, note["tags"])
        if score <= 0:
            continue
        scored.append((score, note))
    scored.sort(key=lambda item: (-item[0], item[1]["title"]))
    return [note for _, note in scored[:limit]]


def strip_section(body: str, heading: str) -> str:
    pattern = rf"\n{re.escape(heading)}[\s\S]*$"
    return re.sub(pattern, "", body).rstrip() + "\n"


def build_link_map(catalog: list[dict]) -> dict[str, str]:
    link_map: dict[str, str] = {}
    for note in catalog:
        for key in [note["title"], note["slug"], note["stem"], *note["aliases"]]:
            if key:
                link_map[key.lower()] = note["title"]
    return link_map


def resolved_link_titles(body: str, link_map: dict[str, str], self_title: str) -> set[str]:
    titles: set[str] = set()
    for raw in existing_wikilinks(body):
        title = link_map.get(raw.lower())
        if title and title != self_title:
            titles.add(title)
    return titles


def format_pairs_clause(titles: list[str]) -> str:
    links = [f"[[{title}]]" for title in titles]
    if len(links) == 1:
        return links[0]
    if len(links) == 2:
        return f"{links[0]} and {links[1]}"
    return ", ".join(links[:-1]) + f", and {links[-1]}"


def pick_link_candidates(
    stem: str,
    title: str,
    tags: list[str],
    catalog: list[dict],
    exclude: set[str],
    needed: int,
) -> list[str]:
    picks: list[str] = []
    for note in related_notes(stem, title, tags, catalog, limit=15):
        if not is_linkable(note):
            continue
        candidate = note["title"]
        if candidate not in exclude and candidate != title and candidate not in picks:
            picks.append(candidate)
        if len(picks) >= needed:
            return picks
    for note in catalog:
        if note["stem"] == stem or not is_linkable(note):
            continue
        candidate = note["title"]
        if candidate in exclude or candidate == title or candidate in picks:
            continue
        picks.append(candidate)
        if len(picks) >= needed:
            break
    return picks


def ensure_min_body_links(
    body: str,
    stem: str,
    title: str,
    tags: list[str],
    catalog: list[dict],
    link_map: dict[str, str],
    min_links: int = MIN_BODY_LINKS,
) -> str:
    linked = resolved_link_titles(body, link_map, title)
    if len(linked) >= min_links:
        return body

    needed = min_links - len(linked)
    picks = pick_link_candidates(stem, title, tags, catalog, linked | {title}, needed)
    if not picks:
        return body

    clause = format_pairs_clause(picks)
    trimmed = body.rstrip()
    if trimmed.endswith("."):
        trimmed = trimmed[:-1].rstrip()

    if re.search(r"\bPairs with\b", body, re.I):
        body = f"{trimmed}. Also pairs with {clause}."
    else:
        body = f"{trimmed}. Pairs with {clause}."
    return body.rstrip() + "\n"


def build_see_also(
    related: list[dict],
    linked: set[str],
    stem: str,
    title: str,
    catalog: list[dict],
    link_map: dict[str, str],
    body: str,
    min_total: int = MIN_OUTGOING_LINKS,
) -> str:
    picked: list[dict] = []
    picked_titles: set[str] = set()
    resolved = resolved_link_titles(body, link_map, title)

    def consider(note: dict) -> None:
        note_title = note["title"]
        if note_title in resolved or note_title in picked_titles or note_title == title:
            return
        if note_title in linked:
            return
        picked.append(note)
        picked_titles.add(note_title)

    for note in related:
        consider(note)

    while len(resolved | picked_titles) < min_total:
        added = False
        for note in catalog:
            if note["stem"] == stem or not is_linkable(note):
                continue
            before = len(picked_titles)
            consider(note)
            if len(picked_titles) > before:
                added = True
                break
        if not added:
            break

    if not picked:
        return ""

    lines = [SEE_ALSO_HEADING, ""]
    for note in picked:
        shared = ", ".join(sorted(set(note.get("_shared", [])))[:3])
        if shared:
            lines.append(f"- [[{note['title']}]] — {shared}")
        else:
            lines.append(f"- [[{note['title']}]]")
    return "\n".join(lines) + "\n"


def build_moc_body(catalog: list[dict]) -> str:
    clusters: dict[str, list[str]] = {
        "Foundations": [
            "pkm",
            "building-a-second-brain",
            "atomic-notes",
            "maps-of-content",
            "getting-started",
        ],
        "Capture": [
            "capture",
            "context-aware-capture",
            "analog-capture-tools",
            "mobile-capture-workflows",
            "the-trusted-inbox",
            "newsletter-filtering",
            "signal-vs-noise",
        ],
        "Organize": [
            "para-method",
            "gtd-vs-para",
            "organization",
            "the-archive-method",
            "metadata-strategy",
            "daily-notes",
        ],
        "Distill & review": [
            "progressive-summarization",
            "weekly-review-checklists",
            "periodic-knowledge-review",
            "evergreen-notes",
            "evergreen-vs-fleeting-notes",
            "serendipitous-resurfacing",
        ],
        "Connect & explore": [
            "associative-linking",
            "the-power-of-interconnectivity",
            "graph-view-analytics",
            "digital-serendipity",
            "mind-mapping",
            "visual-thinking",
        ],
        "Express": [
            "creative-output",
            "distraction-free-writing",
            "drafting-in-public",
            "from-note-to-book",
            "synthesis-as-a-goal",
            "creative-blocks",
        ],
        "Systems & tools": [
            "digital-garden",
            "advantages-of-digital-gardens",
            "local-first-software",
            "future-proofing-knowledge",
            "privacy-and-data-sovereignty",
            "e2ee-security",
        ],
    }

    by_stem = {note["stem"]: note for note in catalog}
    lines = [
        "**Maps of Content (MOCs)** are hub notes that index related ideas. Use this page to wander the garden.",
        "",
        MOC_HEADING,
        "",
    ]
    for cluster, stems in clusters.items():
        lines.append(f"### {cluster}")
        lines.append("")
        for stem in stems:
            note = by_stem.get(stem)
            if note:
                lines.append(f"- [[{note['title']}]]")
        lines.append("")

    lines.extend(
        [
            SEE_ALSO_HEADING,
            "",
            "- [[Getting Started]]",
            "- [[PKM]]",
            "- [[Building a Second Brain]]",
            "",
        ]
    )
    return "\n".join(lines)


def update_frontmatter_aliases(inner: str, aliases: list[str]) -> str:
    block = yaml_list(aliases)
    if re.search(r"^aliases:", inner, re.M):
        return re.sub(r"^aliases:.*$", block, inner, count=1, flags=re.M)
    return inner + "\n" + block


def load_catalog() -> list[dict]:
    catalog: list[dict] = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        _, inner, body = split_frontmatter(text)
        title = parse_scalar(inner, "title")
        slug = parse_scalar(inner, "slug") or path.stem
        tags = parse_yaml_list(inner, "tags")
        aliases = parse_yaml_list(inner, "aliases")
        layout = parse_scalar(inner, "layout")
        note_kind = parse_scalar(inner, "note_kind") or "note"
        catalog.append(
            {
                "path": path,
                "stem": path.stem,
                "title": title,
                "slug": slug,
                "tags": tags,
                "aliases": aliases,
                "layout": layout,
                "note_kind": note_kind,
                "body": body,
                "inner": inner,
            }
        )
    return catalog


def is_linkable(note: dict) -> bool:
    if note.get("layout") == "graph":
        return False
    return True


def main() -> None:
    catalog = load_catalog()
    link_targets: list[tuple[str, str]] = []
    for note in catalog:
        link_targets.append((note["title"], note["title"]))
        link_targets.append((note["slug"], note["title"]))
        link_targets.append((note["stem"], note["title"]))
        for alias in note["aliases"]:
            link_targets.append((alias, note["title"]))

    updated = 0
    for note in catalog:
        aliases = suggested_aliases(note["title"], note["slug"], note["aliases"])
        for alias in aliases:
            link_targets.append((alias, note["title"]))

    # dedupe link targets by target string length
    unique_targets: dict[str, str] = {}
    for target, title in link_targets:
        if target not in unique_targets or len(target) > len(unique_targets[target]):
            unique_targets[target] = title
    targets = [(target, title) for target, title in unique_targets.items()]
    link_map = build_link_map(catalog)

    for note in catalog:
        inner = update_frontmatter_aliases(note["inner"], suggested_aliases(note["title"], note["slug"], note["aliases"]))

        if note["stem"] == "maps-of-content":
            body = build_moc_body(catalog)
        elif note["stem"] == "getting-started":
            body = strip_section(note["body"], SEE_ALSO_HEADING).rstrip() + "\n"
        else:
            body = strip_section(note["body"], SEE_ALSO_HEADING)
            body = strip_section(body, MOC_HEADING).rstrip() + "\n"
            body = inline_link(body, targets)
            body = ensure_min_body_links(
                body,
                note["stem"],
                note["title"],
                note["tags"],
                catalog,
                link_map,
            )

            related = related_notes(note["stem"], note["title"], note["tags"], catalog)
            for rel in related:
                rel["_shared"] = sorted(set(note["tags"]) & set(rel["tags"]))
            linked = existing_wikilinks(body)
            see_also = build_see_also(
                related,
                linked,
                note["stem"],
                note["title"],
                catalog,
                link_map,
                body,
            )
            if see_also:
                body = body.rstrip() + "\n\n" + see_also

        fm = f"---\n{inner}\n---\n\n"
        note["path"].write_text(fm + body, encoding="utf-8")
        updated += 1
        print(f"updated: {note['path'].name}")

    print(f"\nDone: {updated} notes wired for wikilinks, aliases, and See also sections.")


if __name__ == "__main__":
    main()
