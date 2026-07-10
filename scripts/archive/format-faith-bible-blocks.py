#!/usr/bin/env python3
"""Faith key_concept: bible shortcode + explanation bullet (not inline NASB paragraphs)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
import importlib.util

_migrate = importlib.util.spec_from_file_location(
    "garden_voice_migrate", ROOT / "scripts" / "garden-voice-migrate.py"
)
_gvm = importlib.util.module_from_spec(_migrate)
_migrate.loader.exec_module(_gvm)
decontract = _gvm.decontract

NOTES = ROOT / "content" / "english" / "notes"
EXPLAIN_YAML = ROOT / "data" / "ep-verse-explanations.yaml"

BOOK = (
    r"(?:[1-3]\s+)?(?:Matthew|Mark|Luke|John|Romans|Ephesians|Galatians|"
    r"Deuteronomy|1 Corinthians|2 Corinthians|James|Hebrews|Psalm|Psalms|Proverbs)"
)
NASB_LINE = re.compile(rf" {BOOK} [\d:,\s-]+ NASB1995\s*$")
BIBLE_SC = re.compile(r"^\s*\{\{<\s*bible\b", re.I)
BULLET = re.compile(r"^\s*-\s+")
MALFORMED = re.compile(
    rf'^\s*-\s+"?({BOOK} [\d:,\s-]+) NASB1995\s+-\s+(.+?)"?\s*$'
)
NORM = re.compile(r"[^a-z0-9]+")


def norm(s: str) -> str:
    return NORM.sub("", s.lower())


def load_explains() -> dict[str, list[tuple[str, str]]]:
    data = yaml.safe_load(EXPLAIN_YAML.read_text(encoding="utf-8"))
    out: dict[str, list[tuple[str, str]]] = {}
    for slug, block in data["verses"].items():
        out[slug] = [(e["ref"], e["explain"]) for e in block]
    return out


def git_shortcodes(slug: str) -> list[str]:
    path = f"content/english/notes/{slug}.md"
    try:
        text = subprocess.run(
            ["git", "show", f"HEAD:{path}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError:
        return []
    if "key_concept: |\n" not in text:
        return []
    start = text.index("key_concept: |\n") + len("key_concept: |\n")
    end = text.find("\nexamples:", start)
    if end < 0:
        end = text.find("\nshareable_thought:", start)
    if end < 0:
        return []
    return [
        ln.rstrip()
        for ln in text[start:end].splitlines()
        if BIBLE_SC.match(ln.strip())
    ]


def ref_from_nasb(stripped: str) -> str:
    m = NASB_LINE.search(stripped)
    return m.group(0).strip().replace(" NASB1995", "").strip() if m else ""


def strip_bullet(text: str) -> str:
    return text.strip().lstrip("- ").strip().strip('"')


def find_explain(items: list[tuple[str, str]], ref: str) -> str | None:
    for r, explain in sorted(items, key=lambda x: -len(x[0])):
        if r == ref or ref.startswith(f"{r}:") or ref.startswith(r):
            return explain
        if ":" in ref and r in ref:
            return explain
    return None


def dedupe_block(kc: str) -> str:
    lines = kc.splitlines()
    out: list[str] = []
    prev_bullet = ""
    for raw in lines:
        if BULLET.match(raw):
            bullet = strip_bullet(raw)
            if bullet == prev_bullet:
                continue
            prev_bullet = bullet
        else:
            prev_bullet = ""
        if not raw.strip() and out and not out[-1].strip():
            continue
        out.append(raw.rstrip())
    return "\n".join(out)


def emphasize_refs(sc: str, ref: str) -> list[str]:
    m = re.search(r'emphasize="([^"]+)"', sc)
    if not m:
        return []
    parts = ref.rsplit(" ", 1)
    if len(parts) != 2:
        return []
    book, loc = parts
    ch = loc.split(":")[0].split("-")[0]
    out: list[str] = []
    for e in m.group(1).split(","):
        e = e.strip()
        if not e:
            continue
        out.append(f"{book} {e}" if ":" in e else f"{book} {ch}:{e}")
    return out


def explain_for_shortcode(sc: str, ref: str, items: list[tuple[str, str]]) -> str:
    for er in emphasize_refs(sc, ref):
        ex = find_explain(items, er)
        if ex:
            return ex
    return find_explain(items, ref) or ""


def lines_match(a: str, b: str) -> bool:
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    return na == nb or na in nb or nb in na


def transform_block(kc: str, slug: str, explains: list[tuple[str, str]]) -> str:
    shortcodes = git_shortcodes(slug)
    sc_i = 0
    lines = kc.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        m = MALFORMED.match(raw)
        if m:
            ref, explain = m.group(1), m.group(2)
            sc = shortcodes[sc_i] if sc_i < len(shortcodes) else f'  {{{{< bible "{ref}" >}}}}'
            sc_i += 1
            yaml_ex = find_explain(explains, ref) or explain
            out.append(sc)
            out.append("")
            out.append(f"  - {decontract(yaml_ex)}")
            i += 1
            continue

        if not NASB_LINE.search(stripped):
            out.append(raw.rstrip())
            i += 1
            continue

        ref = ref_from_nasb(stripped)
        sc = shortcodes[sc_i] if sc_i < len(shortcodes) else f'  {{{{< bible "{ref}" >}}}}'
        sc_i += 1
        explain = decontract(explain_for_shortcode(sc, ref, explains))

        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1

        if explain and i < len(lines) and not BULLET.match(lines[i]):
            gloss = strip_bullet(lines[i])
            if lines_match(gloss, explain):
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1

        if explain and i < len(lines) and BULLET.match(lines[i]):
            bullet = strip_bullet(lines[i])
            if lines_match(bullet, explain):
                i += 1

        out.append(sc)
        out.append("")
        if explain:
            out.append(f"  - {explain}")

    text = dedupe_block("\n".join(out))
    text = re.sub(r"\n{3,}", "\n\n", text)
    if kc.endswith("\n"):
        text += "\n"
    return text


def apply_slug(slug: str, explains: dict[str, list[tuple[str, str]]]) -> bool:
    path = NOTES / f"{slug}.md"
    text = path.read_text(encoding="utf-8")
    if "NASB1995" not in text:
        return False
    marker = "key_concept: |\n"
    if marker not in text:
        return False
    start = text.index(marker) + len(marker)
    end = text.find("\nexamples:", start)
    if end < 0:
        return False
    kc = text[start:end]
    items = explains.get(slug, [])
    new_kc = transform_block(kc, slug, items)
    if new_kc == kc:
        return False
    path.write_text(text[:start] + new_kc + text[end:], encoding="utf-8")
    return True


def main() -> None:
    explains = load_explains()
    changed = 0
    for path in sorted(NOTES.glob("*.md")):
        if "NASB1995" not in path.read_text(encoding="utf-8"):
            continue
        if apply_slug(path.stem, explains):
            print(f"updated {path.stem}")
            changed += 1
    fg = (NOTES / "free-grace.md").read_text(encoding="utf-8")
    assert "NASB1995" not in fg.split("key_concept:")[1].split("examples:")[0]
    assert '{{< bible ref="Ephesians 2:8-9"' in fg
    print(f"Done — {changed} note(s) updated")


if __name__ == "__main__":
    main()
