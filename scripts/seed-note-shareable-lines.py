#!/usr/bin/env python3
"""Draft or verify shareable_lines frontmatter on garden notes (4 lines, max 130 chars)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import (
    dump_frontmatter,
    ensure_terminal_punct,
    is_complete_shareable_line,
    shareable_lines_overlap,
    split_frontmatter,
    _looks_like_title_fragment,
)

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}
MAX_LINE = 130
LINE_COUNT = 4
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]+)?\]\]")
SKIP_LINE = re.compile(r"^\s*\|")
META_SKIP = re.compile(
    r"^(Tension with|Pairs with|More on|See also|Utility surface|link by URL|Each note below|Faith parallel:|Missing note|Pipe wikilink|Unlinked mention|Structure issues|Frontmatter and flashcards)\b",
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
        if not is_complete_shareable_line(line):
            continue
        if any(lines_overlap(line, existing) for existing in picked):
            continue
        picked.append(line)
        if len(picked) >= count:
            break
    return picked


def plain(text: str) -> str:
    text = WIKILINK.sub(r"\1", text)
    return " ".join(text.split())


def clamp(text: str, limit: int = MAX_LINE) -> str:
    text = plain(ensure_terminal_punct(text))
    if len(text) <= limit:
        return text
    # ponytail: drop overlong sentences instead of ellipsis fragments
    return ""


def clean_raw(raw: str) -> str:
    line = raw.strip().lstrip("- ")
    if not line or SKIP_LINE.match(raw) or TABLE_MARK.search(line):
        return ""
    line = plain(line.replace("**", "").replace("`", "").replace("*", ""))
    line = TENSION_TAIL.sub("", line).strip()
    return line


def _principle_sources(fm: dict) -> list[tuple[int, str]]:
    """(priority, text) — description first, then key_concept blocks."""
    out: list[tuple[int, str]] = []
    desc = fm.get("description")
    if isinstance(desc, str) and desc.strip():
        out.append((0, desc.strip()))
    key_concept = fm.get("key_concept")
    if isinstance(key_concept, str) and key_concept.strip():
        for block in key_concept.strip().split("\n\n"):
            block = block.strip()
            if block and not TABLE_MARK.search(block):
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
    """Split on dash when both sides read as standalone principles."""
    for sep in (" - ", " — ", " – "):
        if sep not in sentence:
            continue
        head, tail = sentence.split(sep, 1)
        head, tail = clean_raw(head), clean_raw(tail)
        if not head or not tail:
            continue
        head_c = clamp(head)
        if not head_c or not is_complete_shareable_line(head_c):
            continue
        if _looks_like_title_fragment(head_c):
            continue
        tail_text = tail
        if tail_text.lower().startswith("not "):
            pass
        elif not tail_text[0].isupper():
            tail_text = tail_text[0].upper() + tail_text[1:]
        if not tail_text.endswith((".", "!", "?")):
            tail_text += "."
        tail_c = clamp(tail_text)
        if not tail_c or not is_complete_shareable_line(tail_c):
            continue
        if lines_overlap(head_c, tail_c):
            return [head_c]
        return [head_c, tail_c]
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
        if META_SKIP.match(line):
            return
        if "when the opposite frame fits" in line.lower():
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
    else:
        if flat in seen:
            seen.discard(flat)
            if flat in out:
                out.remove(flat)
    for sentence in sentences:
        add(sentence)
        for half in _contrast_halves(sentence):
            add(half)
    return out


def draft_shareable_lines(fm: dict) -> list[str]:
    """Four distinct quotable lines from description + key_concept only (no examples)."""
    tier_desc: list[str] = []
    tier_key: list[str] = []
    tier_contrast: list[str] = []

    for priority, source in _principle_sources(fm):
        flat = clean_raw(source)
        if not flat:
            continue
        for cand in _candidates_from_text(source):
            if priority == 0:
                tier_desc.append(cand)
            else:
                tier_key.append(cand)
        for sentence in _sentences(flat):
            for half in _contrast_halves(sentence):
                if priority == 0:
                    tier_contrast.append(half)
                else:
                    tier_contrast.append(half)

    for candidate in (
        pick_distinct(tier_desc + tier_key),
        pick_distinct(tier_desc + tier_key + tier_contrast),
        pick_distinct(tier_desc + tier_contrast + tier_key),
        pick_distinct(tier_key + tier_desc),
    ):
        if len(candidate) >= LINE_COUNT:
            return candidate[:LINE_COUNT]
    return pick_distinct(tier_desc + tier_key + tier_contrast)[:LINE_COUNT]


def lint_shareable_lines(path: Path, fm: dict) -> list[str]:
    if path.name in SKIP:
        return []
    lines = fm.get("shareable_lines")
    if not isinstance(lines, list) or len(lines) != LINE_COUNT:
        return [f"FAIL shareable_lines need {LINE_COUNT} items: {path.name}"]
    errs: list[str] = []
    for i, line in enumerate(lines):
        if not isinstance(line, str) or not line.strip():
            errs.append(f"FAIL shareable_lines[{i}] empty: {path.name}")
            continue
        if len(line) > MAX_LINE:
            errs.append(f"FAIL shareable_lines[{i}] {len(line)} chars (max {MAX_LINE}): {path.name}")
        if "[[" in line:
            errs.append(f"FAIL wikilink in shareable_lines[{i}]: {path.name}")
        if not is_complete_shareable_line(line):
            errs.append(f"FAIL shareable_lines[{i}] fragment: {path.name}")
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if isinstance(lines[i], str) and isinstance(lines[j], str) and lines_overlap(lines[i], lines[j]):
                errs.append(f"FAIL shareable_lines[{i}] overlaps [{j}]: {path.name}")
    return errs


def write_shareable_lines(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = yaml.safe_load(raw_fm) or {}
    if not isinstance(fm, dict):
        return False
    fm["shareable_lines"] = draft_shareable_lines(fm)
    new_text = f"---\n{dump_frontmatter(fm)}\n---{body}"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def _self_check() -> None:
    sample = {
        "title": "Capture",
        "description": "Save what resonates into one inbox I trust - then empty it weekly.",
        "key_concept": "Friction kills capture.\n\nOne inbox, weekly process. Resonance is the filter, not FOMO.",
        "examples": ["Jeepney spark on a receipt - one pocket notebook, no sorting yet."],
    }
    lines = draft_shareable_lines(sample)
    assert len(lines) == 4
    assert all(len(t) <= MAX_LINE for t in lines)
    assert all("[[" not in t for t in lines)
    assert all(is_complete_shareable_line(t) for t in lines)
    assert len(lines) == len(pick_distinct(lines))
    errs = lint_shareable_lines(Path("capture.md"), {"shareable_lines": lines})
    assert not errs
    repent = {
        "description": "Jesus' opening command: turn from self-rule and trust the good news that the kingdom is at hand.",
        "key_concept": (
            "Repentance is a change of mind and direction - not a down payment on salvation.\n\n"
            "Belief is reliance on Christ's promise, not mere intellectual agreement. "
            "Under Free Grace, this pair is how life begins: receive the kingdom as gift, "
            "then live under the King's rule in response."
        ),
    }
    rlines = draft_shareable_lines(repent)
    assert len(rlines) == 4
    assert all(is_complete_shareable_line(t) for t in rlines)
    assert not any(t.lower().startswith("not ") for t in rlines[1:])


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("seed-note-shareable-lines self-check OK")
        return 0

    check_only = "--check" in sys.argv
    bad = 0
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        raw_fm, _ = split_frontmatter(text)
        fm = yaml.safe_load(raw_fm) or {}
        if not isinstance(fm, dict):
            continue
        if check_only:
            for msg in lint_shareable_lines(path, fm):
                print(msg)
                bad += 1
            continue
        if write_shareable_lines(path):
            changed += 1

    if check_only:
        if bad:
            print(f"\n{bad} shareable_lines lint issue(s)")
            return 1
        print("Note shareable_lines lint OK")
        return 0

    print(f"Wrote shareable_lines on {changed} note(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
