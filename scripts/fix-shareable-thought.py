#!/usr/bin/env python3
"""Regenerate shareable_thought from description + key_concept (4 lines, max 130 chars)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import (
    dump_frontmatter,
    ensure_terminal_punct,
    gets_point_across,
    is_complete_shareable_line,
    shareable_lines_overlap,
    split_frontmatter,
    _looks_like_title_fragment,
    INCOMPLETE_SPLIT_HEAD,
)

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}
MAX_LINE = 130
LINE_COUNT = 4
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]+)?\]\]")
BIBLE_RE = re.compile(r"^\{\{<\s*bible\b", re.I)
SKIP_LINE = re.compile(r"^\s*\|")
META_SKIP = re.compile(
    r"^(Tension with|Pairs with|More on|See also|Utility surface|link by URL|Each note below|Faith parallel:|Missing note|Pipe wikilink|Unlinked mention|Structure issues|Frontmatter and flashcards|Garden parallel)\b",
    re.I,
)
TENSION_TAIL = re.compile(r"\.\s*Tension with\b.*", re.I | re.S)
TABLE_MARK = re.compile(r"\|.+\|")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def lines_overlap(a: str, b: str) -> bool:
    return shareable_lines_overlap(a, b)


def pick_distinct(candidates: list[str], count: int = LINE_COUNT) -> list[str]:
    picked: list[str] = []
    for line in candidates:
        if not gets_point_across(line):
            continue
        if any(lines_overlap(line, existing) for existing in picked):
            continue
        picked.append(line)
        if len(picked) >= count:
            break
    return picked


def plain(text: str) -> str:
    text = WIKILINK.sub(r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return " ".join(text.split())


def clamp(text: str, limit: int = MAX_LINE) -> str:
    text = plain(ensure_terminal_punct(text))
    if len(text) <= limit:
        return text
    return ""


def clean_raw(raw: str) -> str:
    line = raw.strip().lstrip("- ")
    if not line or SKIP_LINE.match(raw) or TABLE_MARK.search(line):
        return ""
    if BIBLE_RE.match(line):
        return ""
    line = plain(line.replace("**", "").replace("`", "").replace("*", ""))
    line = TENSION_TAIL.sub("", line).strip()
    return line


def _principle_sources(fm: dict) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    desc = fm.get("description")
    if isinstance(desc, str) and desc.strip():
        out.append((0, desc.strip()))
    key_concept = fm.get("key_concept")
    if isinstance(key_concept, str) and key_concept.strip():
        for block in key_concept.strip().split("\n\n"):
            block = block.strip()
            if not block or TABLE_MARK.search(block) or BIBLE_RE.match(block):
                continue
            if block.startswith("- "):
                block = block[2:]
            out.append((1, block.replace("\n", " ")))
    return out


def _sentences(flat: str) -> list[str]:
    parts = [clean_raw(p) for p in SENTENCE_SPLIT.split(flat) if clean_raw(p)]
    merged: list[str] = []
    for part in parts:
        if re.match(r"^\([^)]+\)\.?$", part) and merged:
            merged[-1] = f"{merged[-1]} {part}"
        else:
            merged.append(part)
    return merged if merged else ([flat] if clean_raw(flat) else [])


def _contrast_halves(sentence: str) -> list[str]:
    for sep in (" - ", " — ", " – "):
        if sep not in sentence:
            continue
        head, tail = sentence.split(sep, 1)
        head, tail = clean_raw(head), clean_raw(tail)
        if not head or not tail or INCOMPLETE_SPLIT_HEAD.search(head):
            continue
        head_c = clamp(head)
        if not head_c or not is_complete_shareable_line(head_c) or _looks_like_title_fragment(head_c):
            continue
        tail_text = tail
        if not tail_text.lower().startswith("not ") and not tail_text[0].isupper():
            tail_text = tail_text[0].upper() + tail_text[1:]
        if not tail_text.endswith((".", "!", "?")):
            tail_text += "."
        tail_c = clamp(tail_text)
        if not tail_c or not gets_point_across(tail_c):
            continue
        if lines_overlap(head_c, tail_c):
            return [head_c] if gets_point_across(head_c) else []
        if gets_point_across(head_c) and gets_point_across(tail_c):
            return [head_c, tail_c]
        return [clamp(sentence)] if gets_point_across(clamp(sentence)) else []
    return []


def _candidates_from_text(text: str, *, min_len: int = 12) -> list[str]:
    flat = clean_raw(text)
    if not flat or META_SKIP.match(flat):
        return []
    out: list[str] = []
    seen: set[str] = set()

    def add(raw: str) -> None:
        line = clamp(raw)
        if not line or len(line) < min_len or line in seen:
            return
        if META_SKIP.match(line) or "when the opposite frame fits" in line.lower():
            return
        if not gets_point_across(line):
            return
        seen.add(line)
        out.append(line)

    sentences = _sentences(flat)
    contrast_parts: list[str] = []
    for sentence in sentences:
        contrast_parts.extend(_contrast_halves(sentence))

    if len(contrast_parts) >= 2:
        for half in contrast_parts:
            add(half)
    elif len(sentences) <= 1:
        add(flat)
    for sentence in sentences:
        add(sentence)
        for half in _contrast_halves(sentence):
            add(half)
    return out


def draft_shareable_thought(fm: dict) -> list[str]:
    tier_desc: list[str] = []
    tier_key: list[str] = []
    tier_contrast: list[str] = []

    for priority, source in _principle_sources(fm):
        flat = clean_raw(source)
        if not flat:
            continue
        for cand in _candidates_from_text(source):
            (tier_desc if priority == 0 else tier_key).append(cand)
        for sentence in _sentences(flat):
            for half in _contrast_halves(sentence):
                tier_contrast.append(half)

    for candidate in (
        pick_distinct(tier_desc + tier_key),
        pick_distinct(tier_desc + tier_key + tier_contrast),
        pick_distinct(tier_desc + tier_contrast + tier_key),
        pick_distinct(tier_key + tier_desc),
        pick_distinct(tier_contrast + tier_desc + tier_key),
    ):
        if len(candidate) >= LINE_COUNT:
            return candidate[:LINE_COUNT]
    return pick_distinct(tier_desc + tier_key + tier_contrast)[:LINE_COUNT]


def write_shareable_thought(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = yaml.safe_load(raw_fm) or {}
    if not isinstance(fm, dict):
        return False
    fm["shareable_thought"] = draft_shareable_thought(fm)
    new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    check_only = "--check" in sys.argv
    only_failing = "--failing" in sys.argv
    bad = 0
    changed = 0

    if check_only or only_failing:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "lint", ROOT / "scripts" / "lint-notes-frontmatter.py"
        )
        lint = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lint)

    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, _ = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        if only_failing:
            errs = lint.lint_shareable_thought(path, fm)
            if not errs:
                continue
        if check_only:
            for msg in lint.lint_shareable_thought(path, fm):
                print(msg)
                bad += 1
            continue
        if write_shareable_thought(path):
            changed += 1

    if check_only:
        if bad:
            print(f"\n{bad} shareable_thought lint issue(s)")
            return 1
        print("Note shareable_thought lint OK")
        return 0

    print(f"Wrote shareable_thought on {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
