#!/usr/bin/env python3
"""Split overlong key_concept bullets into shorter items."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}

BIBLE_RE = re.compile(r"^\{\{<\s*bible\b", re.I)
TABLE_RE = re.compile(r"^\|")
BULLET_RE = re.compile(r"^-\s+")
MAX_WORDS = 25
MAX_CHARS = 180
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[\(\"\'])|(?<=\.)\s+(?=\[\[)")
PREFIX_SPLIT = re.compile(
    r"\s+(?=(?:PKM mirror|Garden parallel|Faith parallel|Same shape|Same math|Same logic|Same move|Same rhythm|More on|Goes further|When it fits|When it doesn't|Ops I don't|What I quote|Showroom branch|Git lesson|Where free breaks|Hard caps|Good fits|Bad fits|Updates that|Still say no|Guiding principle|The question|But God,)\b)",
    re.I,
)
COLON_TAIL = re.compile(r"^(.{8,60}?):\s+(.+)$")
SCRIPTURE_TAIL = re.compile(r"(?<=[.!?])\s+(?=But\b)")
BOLD_DEF_SPLIT = re.compile(r"(?<=\.)\s+(?=\*\*[^*]+\*\*\s*=)")
BOLD_LABEL_SPLIT = re.compile(r"\s+(?=\*\*[^*]{3,}:\*\*)")
WIKI_SPLIT = re.compile(r"(?<=[.;!?])\s+(?=\[\[)")
FRAGMENT_START = re.compile(r"^(with|and|or|but|not|so|then|audit|even|he)\b", re.I)


def needs_split(text: str) -> bool:
    return len(text.split()) > MAX_WORDS or len(text) > MAX_CHARS


def _split_once(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    colon = COLON_TAIL.match(text)
    if colon and len(colon.group(2).split()) > MAX_WORDS // 2:
        head = colon.group(1).strip()
        if not head.lower().startswith(("parallel", "pkm", "faith", "garden", "same")):
            return [f"{head}:", colon.group(2).strip()]
    for splitter in (
        PREFIX_SPLIT.split,
        SCRIPTURE_TAIL.split,
        BOLD_DEF_SPLIT.split,
        SENTENCE_SPLIT.split,
        BOLD_LABEL_SPLIT.split,
        WIKI_SPLIT.split,
        lambda t: re.split(r";\s+", t),
    ):
        parts = [p.strip() for p in splitter(text) if p.strip()]
        if len(parts) > 1:
            return parts
    for sep in (" - ", " — ", " – "):
        if sep in text:
            head, tail = text.split(sep, 1)
            head, tail = head.strip(), tail.strip()
            if len(head.split()) >= 6 and len(tail.split()) >= 4:
                return [head, tail]
    return [text]


def merge_fragments(parts: list[str]) -> list[str]:
    if not parts:
        return parts
    merged: list[str] = []
    for part in parts:
        if merged and merged[-1].rstrip().endswith(":"):
            merged[-1] = f"{merged[-1]} {part}"
        elif merged and part[0].islower() and len(part.split()) >= 4:
            merged.append(part)
        elif merged and (
            part[0].islower()
            or FRAGMENT_START.match(part)
            or (part.startswith("(") and len(part.split()) < 12)
        ):
            merged[-1] = f"{merged[-1]} {part}"
        else:
            merged.append(part)
    return merged


def split_chunk(text: str, depth: int = 0) -> list[str]:
    text = text.strip()
    if not text or depth > 6:
        return [text] if text else []
    if not needs_split(text):
        return [text]
    parts = merge_fragments(_split_once(text))
    if len(parts) == 1:
        return [text]
    out: list[str] = []
    for part in parts:
        out.extend(split_chunk(part, depth + 1) if needs_split(part) else [part])
    return merge_fragments(out) or [text]


def split_bullet(text: str) -> list[str]:
    return merge_fragments(split_chunk(text.strip()))


def bulletize_key_concept(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    splits = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if out and out[-1] != "":
                out.append("")
            continue
        if BIBLE_RE.match(stripped) or TABLE_RE.match(stripped):
            out.append(stripped)
            continue
        if BULLET_RE.match(stripped):
            content = stripped[2:].strip()
            pieces = split_bullet(content)
            if len(pieces) > 1:
                splits += 1
            for piece in pieces:
                out.append(f"- {piece}")
            continue
        out.append(stripped)
    trimmed: list[str] = []
    for line in out:
        if line == "" and trimmed and trimmed[-1] == "":
            continue
        trimmed.append(line)
    return "\n".join(trimmed).rstrip("\n"), splits


def process_note(path: Path, dry_run: bool = False) -> int:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    fm = yaml.safe_load(raw_fm) or {}
    kc = fm.get("key_concept")
    if not isinstance(kc, str) or not kc.strip():
        return 0
    new_kc, splits = bulletize_key_concept(kc)
    if new_kc == kc.rstrip("\n"):
        return 0
    if dry_run:
        return splits
    fm["key_concept"] = new_kc
    path.write_text(f"---\n{dump_frontmatter(fm)}\n---\n{body}", encoding="utf-8")
    return splits


def _self_check() -> None:
    long = (
        "God-centered design asks who the plan ultimately serves before I optimize the slide, the program, or the side project. "
        "[[Seek the Kingdom First]] is the priority filter; [[Love Your Neighbor]] keeps it from becoming selfish spirituality. "
        "PKM mirror: [[People-Centered Design]] serves real human needs; this note orders what I'm building and why."
    )
    parts = split_bullet(long)
    assert len(parts) >= 2
    cms = (
        "More setup than raw markdown (auth, config, media folders) quote it, don't tuck it in theme tweaks. "
        "**When it fits Static Site Client Scope:** one or two non-technical editors, occasional posts, no member login, no cart. "
        "**When it doesn't:** five daily editors with workflows, private content, or make it exactly like our old WordPress admin."
    )
    assert len(split_bullet(cms)) >= 2


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("split-key-concept-bullets self-check OK")
        return 0
    dry_run = "--dry-run" in sys.argv
    total = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        n = process_note(path, dry_run=dry_run)
        if n:
            total += n
    print(f"{'Would split' if dry_run else 'Split'} {total} long bullet(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
