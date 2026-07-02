#!/usr/bin/env python3
"""Lint JoRap voice: AI-tells and plain-word swap candidates in notes/blog prose."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml required for notes-voice-lint")

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = (
    ROOT / "content/english/notes",
    ROOT / "content/english/blog",
)
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

# ponytail: word list only — no NLP; catches obvious thesaurus/AI slop, not context
AI_WORDS = re.compile(
    r"\b("
    r"landscape|delve|leverage|utilize|facilitate|robust|seamless|comprehensive|"
    r"Furthermore|Moreover|Additionally|realm|tapestry|harness|elevate"
    r")\b",
    re.I,
)
AI_PHRASES = re.compile(
    r"(In today'?s fast-paced world|Let'?s dive in|Whether you'?re a beginner|"
    r"game-?changer|It'?s worth noting|In conclusion|Unlock the full potential|"
    r"Without further ado|When it comes to|In the realm of|delve into|"
    r"navigate the (world|landscape)|comprehensive guide)",
    re.I,
)
GLOSS_HINTS = re.compile(r"\b(unmerited favor)\b", re.I)

NOTE_FIELDS = ("title", "meta_title", "description", "key_concept")
SKIP_NOTE_KINDS = {"meta", "index"}


def load_md(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    return meta, text[match.end() :]


def prose_chunks(meta: dict, body: str, *, notes: bool) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    if notes:
        for key in NOTE_FIELDS:
            val = meta.get(key)
            if isinstance(val, str) and val.strip():
                chunks.append((key, val))
        for key in ("examples", "aliases"):
            val = meta.get(key)
            if isinstance(val, list):
                for i, item in enumerate(val):
                    if isinstance(item, str) and item.strip():
                        chunks.append((f"{key}[{i}]", item))
        for i, card in enumerate(meta.get("cards") or []):
            if not isinstance(card, dict):
                continue
            for side in ("front", "back"):
                val = card.get(side)
                if isinstance(val, str) and val.strip():
                    chunks.append((f"cards[{i}].{side}", val))
        for row in meta.get("relationships") or []:
            if isinstance(row, dict):
                reason = row.get("reason")
                if isinstance(reason, str) and reason.strip():
                    chunks.append(("relationships.reason", reason))
    else:
        for key in ("title", "meta_title", "description", "summary"):
            val = meta.get(key)
            if isinstance(val, str) and val.strip():
                chunks.append((key, val))
        if body.strip():
            chunks.append(("body", body))
    return chunks


GLOSS_FIELDS = frozenset(
    {
        "description",
        "key_concept",
        "examples",
        "cards",
        "relationships.reason",
        "body",
    }
)


def lint_text(field: str, text: str) -> list[str]:
    issues: list[str] = []
    for match in AI_WORDS.finditer(text):
        issues.append(f"{field}: AI-tell word `{match.group(0)}`")
    if AI_PHRASES.search(text):
        issues.append(f"{field}: AI-slop phrase")
    base = field.split("[", 1)[0]
    if base in GLOSS_FIELDS or field.startswith("examples[") or field.startswith("cards["):
        for match in GLOSS_HINTS.finditer(text):
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 80)
            window = text[start:end].lower()
            if any(token in window for token in ("earned", "gift", "deserved", "didn't earn", "never earned")):
                continue
            issues.append(
                f"{field}: `{match.group(0)}` — add plain gloss (e.g. gift you didn't earn)"
            )
    return issues


def lint_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    meta, body = load_md(path)
    notes = path.parent.name == "notes"
    if notes:
        if meta.get("draft"):
            return []
        if meta.get("note_kind", "note") in SKIP_NOTE_KINDS:
            return []
    elif meta.get("draft"):
        return []

    errors: list[str] = []
    for field, text in prose_chunks(meta, body, notes=notes):
        for issue in lint_text(field, text):
            errors.append(f"{rel}: {issue}")
    return errors


def _self_check() -> None:
    assert AI_WORDS.search("navigate the landscape")
    assert AI_PHRASES.search("Let's dive in")
    assert not lint_text("t", "plain words only")


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("notes-voice-lint self-check OK")
        return 0

    check_only = "--check" in sys.argv
    errors: list[str] = []
    for content_dir in CONTENT_DIRS:
        if not content_dir.is_dir():
            continue
        for path in sorted(content_dir.glob("*.md")):
            errors.extend(lint_file(path))

    if not errors:
        print("Voice lint OK")
        return 0

    label = "Voice lint warnings" if check_only else "Voice lint"
    print(f"{label}:", file=sys.stderr)
    for err in errors:
        print(f"  {err}", file=sys.stderr)
    return 1 if check_only else 0


if __name__ == "__main__":
    sys.exit(main())
