#!/usr/bin/env python3
"""Expand note bodies to full evergreen claims from frontmatter descriptions."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SKIP = {"_index", "graph", "maps-of-content", "getting-started", "atomic-notes"}
SEE_ALSO = "## See also"

# Timeless rewrites for descriptions that name this site or other dated anchors.
DESC_OVERRIDES: dict[str, str] = {
    "building-a-second-brain": (
        "My brain is for having ideas, not storing them. "
        "A Second Brain is the system that holds them - starting with [[Capture]]."
    ),
    "digital-garden": (
        "My digital garden is a personal site where notes grow in public - "
        "linked, imperfect, alive."
    ),
    "zettelkasten": (
        "Zettelkasten is one idea per note, dense links, writing from the network."
    ),
}

# Wikilink substitutions applied after the body is built (longest matches first).
WIKILINK_FIXES: dict[str, list[tuple[str, str]]] = {
    "capture": [("PKM", "[[PKM]]")],
    "para-method": [("PARA", "[[PARA]]")],
    "zettelkasten": [("one idea per note", "one [[Atomic Notes|atomic]] idea per note")],
    "organization": [(" in PKM isn't", " in [[PKM]] isn't")],
}


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def parse_scalar(block: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*"?([^"\n]+)"?', block, re.M)
    return match.group(1).strip() if match else ""


def lead_text(desc: str) -> str:
    if not desc:
        return desc
    first_word = desc.split()[0] if desc.split() else ""
    if first_word.isupper() and len(first_word) > 1:
        return desc
    if desc[0].isalpha() and desc[0] != "I":
        return desc[0].lower() + desc[1:]
    return desc


def evergreen_body(title: str, description: str, stem: str) -> str:
    desc = DESC_OVERRIDES.get(stem, description).strip()
    if not desc:
        return f"**{title}**."

    if desc.lower().startswith(title.lower()):
        body = f"**{title}**{desc[len(title) :]}"
    else:
        body = f"**{title}** — {lead_text(desc)}"

    for old, new in WIKILINK_FIXES.get(stem, []):
        body = body.replace(old, new)

    body = body.rstrip(".") + "."
    body = re.sub(r"\?\.", ".", body)
    return body


def extract_see_also(body: str) -> str:
    idx = body.find(SEE_ALSO)
    if idx == -1:
        return ""
    return body[idx:].rstrip() + "\n"


def main() -> None:
    updated = 0
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        fm, inner, body = split_frontmatter(text)
        title = parse_scalar(inner, "title")
        description = parse_scalar(inner, "description")
        see_also = extract_see_also(body)
        new_body = evergreen_body(title, description, path.stem)
        path.write_text(f"{fm}\n\n{new_body}\n\n{see_also}", encoding="utf-8")
        updated += 1
        print(f"evergreen: {path.name}")

    print(f"\nDone: {updated} notes updated.")


if __name__ == "__main__":
    main()
