#!/usr/bin/env python3
"""Normalize relationships frontmatter: note_kind index, sort rows, dedupe wikilinks."""

from __future__ import annotations

from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}
INDEX_SLUGS = {"getting-started", "eternal-principles", "maps-of-content"}


def load_fm(raw_fm: str) -> dict:
    data = yaml.safe_load(raw_fm) or {}
    return data if isinstance(data, dict) else {}


def normalize_rows(fm: dict) -> list[dict[str, str]] | None:
    rels = fm.get("relationships")
    if not isinstance(rels, list):
        return None
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in rels:
        if not isinstance(item, dict):
            continue
        wikilink = str(item.get("wikilink", "")).strip()
        key = wikilink.lower()
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "type": str(item.get("type", "")).strip(),
                "wikilink": wikilink,
                "reason": str(item.get("reason", "")).strip(),
            }
        )
    rows.sort(key=lambda r: (r["type"].lower(), r["wikilink"].lower()))
    return rows


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    if not raw_fm:
        return False
    fm = load_fm(raw_fm)
    if fm.get("note_kind") == "meta":
        return False

    changed = False
    slug = path.stem
    if slug in INDEX_SLUGS and fm.get("note_kind") != "index":
        fm["note_kind"] = "index"
        changed = True

    new_rel = normalize_rows(fm)
    if new_rel is not None and new_rel != fm.get("relationships"):
        if new_rel:
            fm["relationships"] = new_rel
        elif "relationships" in fm:
            del fm["relationships"]
        changed = True

    if not changed:
        return False
    out = f"---\n{dump_frontmatter(fm)}\n---{body}"
    if not out.endswith("\n"):
        out += "\n"
    path.write_text(out, encoding="utf-8")
    return True


def main() -> int:
    n = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        if process_file(path):
            n += 1
            print("updated:", path.name)
    print(f"done: {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
