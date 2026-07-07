#!/usr/bin/env python3
"""Insert JoRap-voice explanations after scripture lines in EP key_concept."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content" / "english" / "notes"
EXPLAIN_YAML = ROOT / "data" / "ep-verse-explanations.yaml"

REF_TAIL = re.compile(r"^(?P<head>.*\([^)]+\))\.?\s*(?P<tail>.+)$")
REF_ONLY = re.compile(r"\([^)]+\)")


def load_explanations() -> dict[str, list[tuple[str, str]]]:
    data = yaml.safe_load(EXPLAIN_YAML.read_text(encoding="utf-8"))
    out: dict[str, list[tuple[str, str]]] = {}
    for slug, block in data["verses"].items():
        out[slug] = [(e["ref"], e["explain"]) for e in block]
    return out


def ref_in_line(ref: str, line: str) -> bool:
    return f"({ref})" in line or f"({ref}." in line


def find_explain(slug_items: list[tuple[str, str]], line: str) -> str | None:
    # ponytail: longest ref match wins (Matthew 7:16-20 before 7:16)
    for ref, explain in sorted(slug_items, key=lambda x: -len(x[0])):
        if ref_in_line(ref, line):
            return explain
    return None


def is_explain_line(line: str, explain: str) -> bool:
    s = line.strip()
    if not s or s.startswith("|") or s.startswith("[[") or REF_ONLY.search(s):
        return False
    return explain[:32] in s or s[:32] in explain


def process_block(kc: str, slug_items: list[tuple[str, str]]) -> str:
    lines = kc.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.startswith("  ") or not REF_ONLY.search(raw):
            out.append(raw)
            i += 1
            continue
        stripped = raw[2:]
        m = REF_TAIL.match(stripped)
        if m and m.group("tail").strip():
            head = m.group("head").rstrip()
            if not head.endswith("."):
                head += "."
            tail = m.group("tail").strip()
            out.append(f"  {head}")
            out.append("")
            out.append(f"  {tail}")
            i += 1
            continue
        explain = find_explain(slug_items, stripped)
        out.append(raw.rstrip())
        i += 1
        if explain:
            nxt = lines[i].strip() if i < len(lines) else ""
            if nxt and is_explain_line(lines[i], explain):
                continue
            if nxt and not nxt.startswith("[[") and not REF_ONLY.search(nxt) and not nxt.startswith("|"):
                continue  # already has a gloss line
            out.append("")
            out.append(f"  {explain}")
    return "\n".join(out) + ("\n" if kc.endswith("\n") else "")


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
    # ponytail: spot-check
    fg = (NOTES / "free-grace.md").read_text(encoding="utf-8")
    assert "Hear Christ's word and believe" in fg
    print(f"Done — {changed} note(s) updated")


if __name__ == "__main__":
    main()
