#!/usr/bin/env python3
"""Wrap pre-Examples prose in ## Key Concept; use description when only one opening paragraph."""
from __future__ import annotations

import re
import sys
from pathlib import Path

NOTES_DIR = Path(__file__).resolve().parents[1] / "content" / "english" / "notes"
SKIP = {"_index", "create", "issues"}
NEXT_SECTIONS = ("## Examples", "## Note Relationships", "## See also", "## Maps", "## Theological basis")


def parse_note(text: str) -> tuple[str, str] | tuple[None, None]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def note_kind(fm: str) -> str:
    m = re.search(r'^note_kind:\s*"?(\w+)"?', fm, re.M)
    return m.group(1) if m else "note"


def description(fm: str) -> str:
    m = re.search(r'^description:\s*"(.*)"', fm, re.M)
    return m.group(1).strip() if m else ""


def split_before_next_section(body: str) -> tuple[str, str, str]:
    """Return (opening, matched_heading, rest)."""
    best_idx = len(body)
    best_head = ""
    for head in NEXT_SECTIONS:
        idx = body.find(head)
        if idx != -1 and idx < best_idx:
            best_idx = idx
            best_head = head
    if not best_head:
        return body.rstrip(), "", ""
    opening = body[:best_idx].rstrip()
    rest = body[best_idx:]
    return opening, best_head, rest


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]


def normalize(s: str) -> str:
    s = re.sub(r"\*\*[^*]+\*\*", "", s)
    s = re.sub(r"[^\w\s]", " ", s.lower())
    return " ".join(s.split())


def too_similar(a: str, b: str) -> bool:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    aw, bw = set(na.split()), set(nb.split())
    if not aw or not bw:
        return False
    return len(aw & bw) / len(aw | bw) > 0.82


def parse_relationships(body: str) -> list[tuple[str, str, str]]:
    if "## Note Relationships" not in body:
        return []
    section = body.split("## Note Relationships", 1)[1].split("\n##", 1)[0]
    rows: list[tuple[str, str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or "---" in line or "Relationship" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 3:
            rows.append((parts[0].lower(), parts[1], parts[2]))
    return rows


def kc_from_relationships(rows: list[tuple[str, str, str]]) -> str:
    extends = [r for r in rows if r[0] == "extends"]
    contradicts = [r for r in rows if r[0] == "contradicts"]
    parts: list[str] = []
    if extends:
        link, reason = extends[0][1], extends[0][2].rstrip(".")
        parts.append(f"{reason} ({link}).")
    if contradicts:
        link, reason = contradicts[0][1], contradicts[0][2].rstrip(".")
        if not reason.lower().startswith("when"):
            reason = f"when {reason[0].lower()}{reason[1:]}" if reason else reason
        parts.append(f"Tension with {link} {reason}.")
    return " ".join(parts)


def build_key_concept(
    extra_paras: list[str], desc: str, definition: str, body: str = ""
) -> str:
    if extra_paras:
        return "\n\n".join(extra_paras)
    if desc and not too_similar(definition, desc):
        return desc
    from_rels = kc_from_relationships(parse_relationships(body))
    if from_rels and not too_similar(definition, from_rels):
        return from_rels
    if desc:
        return desc
    return from_rels


def migrate(text: str, *, include_meta: bool = False, refresh: bool = False) -> tuple[str, str]:
    fm, body = parse_note(text)
    if fm is None:
        return text, "unparsed"

    kind = note_kind(fm)
    if kind == "meta" and not include_meta:
        return text, "skip-meta"

    if re.search(r"^## Key Concept\s*$", body, re.M):
        if not refresh:
            return text, "has-kc"
        opening = body.split("## Key Concept", 1)[0].strip()
        kc_old = body.split("## Key Concept", 1)[1].split("\n##", 1)[0].strip()
        paras = split_paragraphs(opening)
        if not paras:
            return text, "empty"
        definition = paras[0]
        if not too_similar(definition, kc_old):
            return text, "has-kc"
        kc = build_key_concept([], description(fm), definition, body)
        if too_similar(definition, kc):
            kc = kc_from_relationships(parse_relationships(body)) or kc
        if not kc or too_similar(definition, kc):
            return text, "still-dupe"
        before_kc, after_kc = body.split("## Key Concept", 1)
        kc_tail = after_kc.split("\n##", 1)
        tail = ("\n##" + kc_tail[1]) if len(kc_tail) > 1 else ""
        new_body = f"{before_kc.rstrip()}\n\n## Key Concept\n\n{kc}{tail}"
        return f"---\n{fm}\n---\n{new_body}", "refreshed"

    opening, next_head, rest = split_before_next_section(body)
    if not next_head:
        return text, "no-section"

    paras = split_paragraphs(opening)
    if not paras:
        return text, "empty"

    definition = paras[0]
    kc = build_key_concept(paras[1:], description(fm), definition, body)
    if not kc:
        return text, "no-kc-content"
    if too_similar(definition, kc):
        kc = kc_from_relationships(parse_relationships(body)) or kc

    new_opening = f"{definition}\n\n## Key Concept\n\n{kc}"
    new_body = f"{new_opening}\n\n{next_head}{rest[len(next_head):]}"
    return f"---\n{fm}\n---\n{new_body}", "updated"


def main() -> int:
    dry = "--dry-run" in sys.argv
    include_meta = "--meta" in sys.argv
    refresh = "--refresh-dupes" in sys.argv
    stats: dict[str, int] = {}

    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP:
            continue
        original = path.read_text(encoding="utf-8")
        new_text, status = migrate(original, include_meta=include_meta, refresh=refresh)
        stats[status] = stats.get(status, 0) + 1
        if status in ("updated", "refreshed") and not dry:
            path.write_text(new_text, encoding="utf-8")
            print(f"{status}: {path.stem}")
        elif status in ("updated", "refreshed") and dry:
            print(f"would {status}: {path.stem}")

    print("---")
    for k in sorted(stats):
        print(f"{k}: {stats[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
