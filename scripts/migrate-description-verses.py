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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notes_content import dump_frontmatter, split_frontmatter

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

BOOKS = (
    r"Matthew|Mark|Luke|John|Romans|Galatians|Ephesians|Philippians|Colossians|"
    r"1\s*(?:Cor|Tim|Pet|John|Sam|Kings|Chron)|2\s*(?:Cor|Tim|Pet|Sam|Kings|Chron)|"
    r"3\s*John|Hebrews|James|Jude|Revelation|Genesis|Exodus|Leviticus|Deuteronomy|"
    r"Psalm|Proverbs|Isaiah|Jeremiah|Acts|Timothy|Titus|Philemon|Peter|Deuteronomy"
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


def normalize_key_concept(kc: str) -> str:
    kc = (kc or "").strip()
    # Drop broken auto-insert lines from earlier yaml.dump runs
    lines = kc.split("\n")
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"(?:\d+:\d+(?:-\d+)?(?:\s*[;,]\s*)?)+", stripped.rstrip(".")):
            continue
        if re.fullmatch(r"(?:[A-Za-z0-9\s.;:-]+(?:\d+:\d+)[A-Za-z0-9\s.;:-]*)+", stripped) and ";" in stripped:
            # standalone ref dump line
            if sum(1 for _ in re.finditer(r"\d+:\d+", stripped)) >= 2:
                continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def ensure_refs_in_key_concept(kc: str, refs: list[str]) -> str:
    kc = normalize_key_concept(kc)
    if not refs:
        return kc
    missing = [r for r in refs if r not in kc]
    if not missing:
        return kc
    block = "; ".join(missing)
    if not kc:
        return block + "."
    parts = kc.split("\n\n", 1)
    head = parts[0].rstrip()
    tail = parts[1] if len(parts) > 1 else ""
    head = f"{head} ({block})."
    return head + ("\n\n" + tail if tail else "")


def process(path: Path, *, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    if not raw_fm:
        return False
    meta = yaml.safe_load(raw_fm) or {}
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return False

    refs = extract_refs(desc)
    new_desc = strip_refs(desc) if refs else desc.strip()
    kc = meta.get("key_concept")
    if not isinstance(kc, str):
        kc = ""
    new_kc = ensure_refs_in_key_concept(kc, refs) if refs else normalize_key_concept(kc)

    changed = new_desc != desc or new_kc != kc
    if not changed:
        return False

    meta["description"] = new_desc
    if isinstance(meta.get("key_concept"), str) or refs:
        meta["key_concept"] = new_kc

    if dry_run:
        print(f"{path.name}: refs={refs}")
        return True

    out = f"---\n{dump_frontmatter(meta)}\n---\n{body.lstrip()}"
    path.write_text(out, encoding="utf-8")
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
