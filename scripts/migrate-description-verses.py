#!/usr/bin/env python3
"""Move Bible refs from description to key_concept; strip refs from description."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml required")

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {
    "_index.md",
    "graph.md",
    "cards.md",
    "review.md",
    "backlinks.md",
    "create.md",
    "issues.md",
    "random-duo.md",
}
FM = re.compile(r"^(---\s*\n.*?\n---)(\s*)", re.DOTALL)

BOOKS = (
    r"Matthew|Mark|Luke|John|Romans|Galatians|Ephesians|Philippians|Colossians|"
    r"1\s*(?:Cor|Tim|Pet|John|Sam|Kings|Chron)|2\s*(?:Cor|Tim|Pet|Sam|Kings|Chron)|"
    r"3\s*John|Hebrews|James|Jude|Revelation|Genesis|Exodus|Leviticus|Deuteronomy|"
    r"Psalm|Proverbs|Isaiah|Jeremiah|Acts|Timothy|Titus|Philemon|Peter"
)
REF = rf"(?:{BOOKS})\s+\d+:\d+(?:-\d+)?"
PAREN_REFS = re.compile(rf"\s*\([^)]*(?:\d+:\d+)[^)]*\)")
INLINE_REFS = re.compile(rf"\s*\b{REF}(?:\s*[;,]\s*(?:{REF}|\d+:\d+(?:-\d+)?))*")


def extract_refs(text: str) -> list[str]:
    found: list[str] = []
    for pat in (PAREN_REFS, INLINE_REFS):
        for m in pat.finditer(text):
            chunk = m.group().strip(" ()")
            if chunk and chunk not in found:
                found.append(chunk)
    return found


def strip_refs(text: str) -> str:
    text = PAREN_REFS.sub("", text)
    text = INLINE_REFS.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;])", r"\1", text)
    if text and text[-1] not in ".!?":
        text += "."
    return text


def first_line(text: str) -> str:
    return (text or "").strip().split("\n", 1)[0].strip()


def ensure_refs_in_key_concept(kc: str, refs: list[str]) -> str:
    if not refs:
        return kc
    missing = [r for r in refs if r not in kc]
    if not missing:
        return kc
    block = "; ".join(missing)
    kc = (kc or "").strip()
    if not kc:
        return block + "."
    lines = kc.split("\n")
    if len(lines) >= 2 and lines[1].strip() == "":
        lines.insert(2, f"  {block}.")
    else:
        lines.insert(1, "")
        lines.insert(2, f"  {block}.")
    return "\n".join(lines)


def dump_meta(meta: dict) -> str:
    return yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000).rstrip()


def process(path: Path, *, dry_run: bool) -> bool:
    raw = path.read_text(encoding="utf-8")
    m = FM.match(raw)
    if not m:
        return False
    meta = yaml.safe_load(m.group(1)[4:-4]) or {}
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return False
    refs = extract_refs(desc)
    if not refs:
        return False

    new_desc = strip_refs(desc)
    kc = meta.get("key_concept")
    if not isinstance(kc, str):
        kc = ""
    new_kc = ensure_refs_in_key_concept(kc, refs)

    if new_desc == desc and new_kc == kc:
        return False

    meta["description"] = new_desc
    if new_kc != kc:
        meta["key_concept"] = new_kc

    if dry_run:
        print(f"{path.name}:")
        print(f"  desc: {desc[:90]}...")
        print(f"  ->   {new_desc[:90]}...")
        print(f"  refs: {refs}")
        return True

    new_fm = "---\n" + dump_meta(meta) + "\n---"
    path.write_text(new_fm + raw[m.end(1) - len(m.group(2)) :], encoding="utf-8")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    n = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        if process(path, dry_run=dry_run):
            n += 1
    print(f"{'Would update' if dry_run else 'Updated'} {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
