#!/usr/bin/env python3
"""Polish key_concept opening lines for note cards (not flashcards)."""

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
FM = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
WIKI = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?\]\]")
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
CODE = re.compile(r"`([^`]+)`")
DICT = re.compile(r"^(?:the |a |an )?\w+ is ", re.I)


def clean(text: str) -> str:
    text = WIKI.sub(r"\1", text)
    text = LINK.sub(r"\1", text)
    text = BOLD.sub(r"\1", text)
    text = CODE.sub(r"\1", text)
    return text.strip()


def score(raw: str) -> int:
    c = clean(raw)
    if len(c) < 12:
        return 9999
    if c.startswith("|") or c.startswith("#"):
        return 9999
    s = len(c)
    if s > 120:
        s += 200
    if s > 160:
        s += 500
    if DICT.match(c):
        s += 40
    if "[[" in raw:
        s += 15
    return s


def candidates(meta: dict) -> list[str]:
    out: list[str] = []
    kc = meta.get("key_concept")
    if isinstance(kc, str):
        for line in kc.splitlines():
            line = line.strip()
            if line:
                out.append(line)
            if len(out) >= 4:
                break
    desc = meta.get("description")
    if isinstance(desc, str) and desc.strip():
        out.append(desc.strip())
    return out


def polish_key_concept(kc: str, best_line: str) -> str:
    lines = kc.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    if not non_empty:
        return best_line
    if non_empty[0].strip() == best_line:
        return kc
    # ponytail: only reorder when line 1 is weak and a better line already exists in block
    rebuilt: list[str] = [best_line, ""]
    for ln in lines:
        s = ln.strip()
        if not s or s == best_line:
            continue
        rebuilt.append(ln)
    return "\n".join(rebuilt).rstrip("\n") + "\n"


def main() -> int:
    apply = "--apply" in sys.argv
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = FM.match(text)
        if not m:
            continue
        meta = yaml.safe_load(m.group(1)) or {}
        if meta.get("draft") or meta.get("note_kind", "note") in ("meta", "index"):
            continue
        kc = meta.get("key_concept")
        if not isinstance(kc, str) or not kc.strip():
            continue
        cands = candidates(meta)
        if len(cands) < 2:
            continue
        first = cands[0]
        best = min(cands, key=score)
        if score(first) <= score(best) + 5:
            continue
        if score(best) >= 9999:
            continue
        new_kc = polish_key_concept(kc, clean(best))
        if new_kc == kc:
            continue
        changed += 1
        print(f"{path.stem}: {clean(first)[:60]}… → {clean(best)[:60]}…")
        if apply:
            import yaml as yaml_mod
            from notes_content import dump_frontmatter, split_frontmatter

            raw_fm, body = split_frontmatter(text)
            meta = yaml_mod.safe_load(raw_fm) or {}
            meta["key_concept"] = new_kc.rstrip("\n")
            new_text = f"---\n{dump_frontmatter(meta)}\n---\n{body.lstrip()}"
            path.write_text(new_text, encoding="utf-8")

    print(f"\n{'Applied' if apply else 'Would update'}: {changed} notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
