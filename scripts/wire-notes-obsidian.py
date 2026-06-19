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
        "Graph View Analytics": ["Graph View"],
        "Evergreen vs Fleeting Notes": ["Evergreen vs Fleeting"],
        "Local-first Software": ["Local First"],
        "Note-Taking for Researchers": ["Research Notes"],
        "The Collector's Fallacy": ["Collector's Fallacy"],
        "The 12 Week Year": ["12 Week Year"],
        "The Feynman Technique": ["Feynman Technique"],
        "The Zettelkasten Myth": ["Zettelkasten Myth"],
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
        "Slip-box History": ["Slip Box", "Slip-box"],
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
    return {m.group(1).strip() for m in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", body)}


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


def build_see_also(related: list[dict], linked: set[str]) -> str:
    lines = [SEE_ALSO_HEADING, ""]
    for note in related:
        if note["title"] in linked:
            continue
        shared = ", ".join(sorted(set(note.get("_shared", [])))[:3])
        if shared:
            lines.append(f"- [[{note['title']}]] — {shared}")
        else:
            lines.append(f"- [[{note['title']}]]")
    if len(lines) == 2:
        return ""
    return "\n".join(lines) + "\n"


def build_moc_body(catalog: list[dict]) -> str:
    clusters: dict[str, list[str]] = {
        "Foundations": [
            "pkm",
            "building-a-second-brain",
            "zettelkasten",
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
        catalog.append(
            {
                "path": path,
                "stem": path.stem,
                "title": title,
                "slug": slug,
                "tags": tags,
                "aliases": aliases,
                "body": body,
                "inner": inner,
            }
        )
    return catalog


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

            related = related_notes(note["stem"], note["title"], note["tags"], catalog)
            for rel in related:
                rel["_shared"] = sorted(set(note["tags"]) & set(rel["tags"]))
            linked = existing_wikilinks(body)
            see_also = build_see_also(related, linked)
            if see_also:
                body = body.rstrip() + "\n\n" + see_also

        fm = f"---\n{inner}\n---\n\n"
        note["path"].write_text(fm + body, encoding="utf-8")
        updated += 1
        print(f"updated: {note['path'].name}")

    print(f"\nDone: {updated} notes wired for wikilinks, aliases, and See also sections.")


if __name__ == "__main__":
    main()
