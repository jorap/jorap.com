#!/usr/bin/env python3
"""Insert JoRap-voice explanations after scripture lines in EP key_concept."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content" / "english" / "notes"
EXPLAIN_YAML = ROOT / "data" / "ep-verse-explanations.yaml"

# ponytail: book chapter:verse only — skips parenthetical asides like (by grace you have been saved)
BOOK_REF_END = re.compile(
    r"\((?:(?:[1-3]\s+)?(?:Matthew|Mark|Luke|John|Romans|Ephesians|Galatians|"
    r"Deuteronomy|1 Corinthians|2 Corinthians|James|Hebrews|Psalm|Psalms|Proverbs)\s+[\d:,\s-]+)"
    r"(?:\s+NASB1995)?\)\."
)
INLINE_AFTER_REF = re.compile(
    r"^(?P<verse>.*\((?:(?:[1-3]\s+)?(?:Matthew|Mark|Luke|John|Romans|Ephesians|Galatians|"
    r"Deuteronomy|1 Corinthians|2 Corinthians|James|Hebrews|Psalm|Psalms|Proverbs)\s+[\d:,\s-]+)"
    r"(?:\s+NASB1995)?\)\.)\s+"
    r"(?P<rest>.+)$"
)
BOGUS_GLOSS = re.compile(r"^\s*\.\s*$")


def load_explanations() -> dict[str, list[tuple[str, str]]]:
    data = yaml.safe_load(EXPLAIN_YAML.read_text(encoding="utf-8"))
    out: dict[str, list[tuple[str, str]]] = {}
    for slug, block in data["verses"].items():
        out[slug] = [(e["ref"], e["explain"]) for e in block]
    return out


def ref_in_line(ref: str, line: str) -> bool:
    return f"({ref})" in line or f"({ref}:" in line or f"({ref}." in line


def find_explain(slug_items: list[tuple[str, str]], ref: str, line: str = "") -> str | None:
    needle = line or f"({ref})"
    for r, explain in sorted(slug_items, key=lambda x: -len(x[0])):
        if r == ref or ref.startswith(f"{r}:") or ref_in_line(r, needle):
            return explain
    return None


def is_gloss_line(line: str, explain: str) -> bool:
    s = line.strip()
    if not s or s.startswith("|") or s.startswith("[[") or BOGUS_GLOSS.match(line):
        return False
    if BOOK_REF_END.search(s):
        return False
    return explain[:32] in s or s[:32] in explain


def next_nonempty(lines: list[str]) -> str:
    for ln in lines:
        if ln.strip():
            return ln.strip()
    return ""


def has_gloss_after(peek: list[str], explain: str) -> bool:
    nxt = next_nonempty(peek)
    return bool(nxt and is_gloss_line(nxt, explain))


def clean_block(kc: str, slug_items: list[tuple[str, str]] | None = None) -> str:
    known = {e for _, e in (slug_items or [])}
    lines = kc.splitlines()
    out: list[str] = []
    prev_stripped = ""
    seen_glosses: set[str] = set()
    for ln in lines:
        if BOGUS_GLOSS.match(ln):
            continue
        stripped = ln.strip()
        if stripped in known:
            if stripped in seen_glosses:
                continue
            seen_glosses.add(stripped)
        if stripped and stripped == prev_stripped:
            continue
        if out and not out[-1].strip() and not stripped:
            continue
        out.append(ln.rstrip())
        if stripped and not BOOK_REF_END.search(stripped) and not stripped.startswith("[["):
            prev_stripped = stripped
        else:
            prev_stripped = ""
    text = "\n".join(out)
    if kc.endswith("\n"):
        text += "\n"
    return text


def split_verse_chunks(stripped: str) -> list[tuple[str, str | None]]:
    matches = list(BOOK_REF_END.finditer(stripped))
    if not matches:
        return []
    chunks: list[tuple[str, str | None]] = []
    pos = 0
    for m in matches:
        chunk = stripped[pos : m.end()].strip()
        inner = m.group(0)
        ref = inner[1:-2].strip().removesuffix(" NASB1995")
        chunks.append((chunk, ref))
        pos = m.end()
    tail = stripped[pos:].strip()
    if tail and tail != ".":
        chunks.append((tail, None))
    return chunks


def emit_verse_block(
    out: list[str],
    verse: str,
    explain: str | None,
    peek: list[str],
) -> None:
    if not verse.endswith("."):
        verse += "."
    out.append(f"  {verse}")
    if not explain or has_gloss_after(peek, explain):
        return
    out.append("")
    out.append(f"  {explain}")


def process_block(kc: str, slug_items: list[tuple[str, str]]) -> str:
    raw_lines = clean_block(kc, slug_items).splitlines()
    out: list[str] = []
    i = 0
    while i < len(raw_lines):
        raw = raw_lines[i]
        if not raw.startswith("  ") or not BOOK_REF_END.search(raw):
            out.append(raw.rstrip())
            i += 1
            continue

        stripped = raw[2:]
        inline = INLINE_AFTER_REF.match(stripped)
        if inline and inline.group("rest").strip() != ".":
            verse = inline.group("verse").strip()
            rest = inline.group("rest").strip()
            ref_m = list(BOOK_REF_END.finditer(verse))[-1]
            ref = ref_m.group(0)[1:-2].strip()
            explain = find_explain(slug_items, ref, verse)
            emit_verse_block(out, verse, explain, raw_lines[i + 1 :])
            out.append("")
            out.append(f"  {rest}")
            i += 1
            continue

        chunks = split_verse_chunks(stripped)
        if not chunks:
            out.append(raw.rstrip())
            i += 1
            continue

        for j, (chunk, ref) in enumerate(chunks):
            if ref is None:
                out.append(f"  {chunk}")
                continue
            explain = find_explain(slug_items, ref, chunk)
            peek = raw_lines[i + 1 :] if j == len(chunks) - 1 else []
            emit_verse_block(out, chunk, explain, peek)
            if j < len(chunks) - 1:
                out.append("")
        i += 1

    text = "\n".join(out)
    if kc.endswith("\n"):
        text += "\n"
    return clean_block(text, slug_items)


def apply_slug(slug: str, slug_items: list[tuple[str, str]]) -> bool:
    path = NOTES / f"{slug}.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    marker = "key_concept: |\n"
    if marker not in text:
        return False
    start = text.index(marker) + len(marker)
    end = text.find("\nexamples:", start)
    if end < 0:
        end = text.find("\nshareable_thought:", start)
    if end < 0:
        end = text.find("\nrelationships:", start)
    if end < 0:
        return False
    kc = text[start:end]
    new_kc = process_block(kc, slug_items)
    if new_kc == kc:
        return False
    path.write_text(text[:start] + new_kc + text[end:], encoding="utf-8")
    return True


def main() -> None:
    explains = load_explanations()
    changed = 0
    for slug, items in explains.items():
        if apply_slug(slug, items):
            print(f"updated {slug}")
            changed += 1
    fg = (NOTES / "free-grace.md").read_text(encoding="utf-8")
    assert "Hear Christ's word and believe" in fg
    assert "\n  .\n" not in fg
    assert fg.count("Hear Christ's word and believe") == 1
    print(f"Done — {changed} note(s) updated")


if __name__ == "__main__":
    main()
