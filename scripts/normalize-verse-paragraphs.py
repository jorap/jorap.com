#!/usr/bin/env python3
"""Normalize EP key_concept: every verse mention → full NASB paragraph on its own line.

Run apply-verse-explanations.py after this script to restore JoRap glosses.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content" / "english" / "notes"
NASB_DATA = ROOT / "data" / "scripture-nasb1995.json"
EXPLAIN_YAML = ROOT / "data" / "ep-verse-explanations.yaml"

BOOK = (
    r"(?:[1-3]\s+)?(?:Matthew|Mark|Luke|John|Romans|Ephesians|Galatians|"
    r"Deuteronomy|1 Corinthians|2 Corinthians|James|Hebrews|Psalm|Psalms|Proverbs)"
)
PAREN_GROUP = re.compile(rf"\(([^)]*{BOOK}[^)]*)\)\.?")
REF_SUFFIX = re.compile(rf" ({BOOK} [\d:,\s-]+) NASB1995\.?$")


def load_nasb() -> dict[str, str]:
    import json

    raw = json.loads(NASB_DATA.read_text(encoding="utf-8"))["verses"]
    out: dict[str, str] = {}
    for k, v in raw.items():
        if isinstance(v, dict) and "text" in v:
            out[k] = v["text"]
        elif isinstance(v, dict) and "nasb1995" in v:
            out[k] = v["nasb1995"]["verse"]
    return out


def load_slugs() -> list[str]:
    return list(yaml.safe_load(EXPLAIN_YAML.read_text(encoding="utf-8"))["verses"])


def resolve_ref(ref: str, nasb: dict[str, str]) -> tuple[str, str] | None:
    ref = ref.strip().replace(" NASB1995", "")
    if ref in nasb:
        return ref, nasb[ref]
    best_key = None
    for key in nasb:
        if ref == key or ref.startswith(f"{key}:") or key.startswith(ref):
            if best_key is None or len(key) > len(best_key):
                best_key = key
    return (best_key, nasb[best_key]) if best_key else None


def parse_refs_from_inner(inner: str) -> list[str]:
    inner = inner.replace(" NASB1995", "").strip()
    refs: list[str] = []
    book: str | None = None
    for semi in inner.split(";"):
        for seg in semi.split(","):
            seg = re.sub(r"\s+", " ", seg.strip())
            if not seg:
                continue
            if re.match(rf"^{BOOK}\s+\d", seg):
                refs.append(seg)
                m = re.match(rf"^({BOOK})", seg)
                book = m.group(1) if m else book
            elif book and re.match(r"^[\d]", seg):
                refs.append(f"{book} {seg}")
    return refs


def refs_on_line(stripped: str) -> list[str]:
    found: list[str] = []
    for m in PAREN_GROUP.finditer(stripped):
        found.extend(parse_refs_from_inner(m.group(1)))
    m = REF_SUFFIX.search(stripped)
    if m:
        found.append(m.group(1).strip())
    return found


def verse_line(canonical: str, text: str) -> str:
    return f"  {text} {canonical} NASB1995"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def strip_refs(text: str) -> str:
    cleaned = PAREN_GROUP.sub("", text)
    cleaned = REF_SUFFIX.sub("", cleaned)
    return re.sub(r"\s{2,}", " ", cleaned).strip(" .,;")


def merge_broken_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("  ") and ln.rstrip() and ln.rstrip()[-1] not in ".!?":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].startswith("  "):
                nxt = lines[j].lstrip()
                if nxt[:1] in ";," or (nxt and nxt[0].islower()):
                    out.append(ln.rstrip() + " " + nxt)
                    i = j + 1
                    continue
        out.append(ln)
        i += 1
    return out


def is_duplicate_paraphrase(stripped: str, canon: str) -> bool:
    body = strip_refs(stripped)
    if not body or "[[" in stripped:
        return False
    nbody, ncanon = norm(body), norm(canon)
    if len(nbody) < 20:
        return False
    return ncanon[:50] in nbody or nbody[:50] in ncanon


def emit_verse(canonical: str, text: str, seen: set[str], out: list[str]) -> None:
    if canonical in seen:
        return
    if out and out[-1].strip():
        out.append("")
    out.append(verse_line(canonical, text))
    seen.add(canonical)


def normalize_block(kc: str, nasb: dict[str, str]) -> str:
    lines = merge_broken_lines(kc.splitlines())
    out: list[str] = []
    seen: set[str] = set()

    for raw in lines:
        if not raw.startswith("  "):
            out.append(raw.rstrip())
            continue
        stripped = raw[2:]
        if not stripped.strip():
            out.append("")
            continue

        line_refs = refs_on_line(stripped)
        resolved = [resolve_ref(r, nasb) for r in line_refs]
        resolved = [x for x in resolved if x]

        if len(resolved) == 1 and "[[" not in stripped:
            canonical, text = resolved[0]
            body = strip_refs(stripped)
            if not body or norm(body)[:40] in norm(text) or norm(text)[:40] in norm(body):
                emit_verse(canonical, text, seen, out)
                continue

        if resolved:
            for canonical, text in resolved:
                emit_verse(canonical, text, seen, out)
            body = strip_refs(stripped)
            if body:
                # drop partial quote if full verse already emitted
                skip = any(is_duplicate_paraphrase(body, nasb[k]) for k in seen)
                if not skip:
                    if out and out[-1].strip():
                        out.append("")
                    out.append(f"  {body}")
            continue

        # Paraphrase only — skip if we already have that verse
        if any(is_duplicate_paraphrase(stripped, nasb[k]) for k in seen):
            continue

        out.append(raw.rstrip())

    # ponytail: drop consecutive duplicate verse lines
    deduped: list[str] = []
    prev_verse = ""
    for ln in out:
        if REF_SUFFIX.search(ln.rstrip()) and ln == prev_verse:
            continue
        deduped.append(ln)
        prev_verse = ln if REF_SUFFIX.search(ln.rstrip()) else ""

    text = "\n".join(deduped)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if kc.endswith("\n"):
        text += "\n"
    return text


def apply_slug(slug: str, nasb: dict[str, str]) -> bool:
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
        return False
    kc = text[start:end]
    new_kc = normalize_block(kc, nasb)
    if new_kc == kc:
        return False
    path.write_text(text[:start] + new_kc + text[end:], encoding="utf-8")
    return True


def main() -> None:
    nasb = load_nasb()
    changed = 0
    for slug in load_slugs():
        if apply_slug(slug, nasb):
            print(f"updated {slug}")
            changed += 1
    # ponytail: spot-check
    fg = (NOTES / "free-grace.md").read_text(encoding="utf-8")
    assert "Ephesians 2:8-9 NASB1995" in fg
    assert fg.count("Ephesians 2:8-9 NASB1995") == 1
    assert " NASB1995)." not in fg
    print(f"Done — {changed} note(s) updated")


if __name__ == "__main__":
    main()
