#!/usr/bin/env python3
"""Replace key_concept Gospel/Acts NASB1995 verse lines with {{< jesus-words >}} shortcodes."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content" / "english" / "notes"
JW = yaml.safe_load((ROOT / "data" / "jesus-words.yaml").read_text(encoding="utf-8"))["verses"]

GOSPEL = re.compile(
    r"^  (.+?) (Matthew|Mark|Luke|John|Acts) ([\d:,\s-]+) NASB1995\s*$"
)
SPECIAL: dict[str, tuple[str, str]] = {"Matthew 18": ("Matthew 18:32-33", "Matthew 18")}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def join_words(refs: list[str]) -> str:
    return " ".join(JW[r]["nasb1995"]["words"] for r in refs if r in JW)


def expand(book: str, part: str) -> list[str]:
    part = part.strip()
    if re.fullmatch(r"\d+", part):
        return []
    if "-" not in part:
        return [f"{book} {part}"]
    left, right = part.split("-", 1)
    if ":" in left:
        ch, v1 = left.split(":", 1)
        v2 = right.split(":")[-1]
        return [f"{book} {ch}:{v}" for v in range(int(v1), int(v2) + 1)]
    return []


def lookup_range(book: str, refs: list[str]) -> str:
    if len(refs) == 1:
        return refs[0]
    ch = refs[0].split(":")[0].split()[1]
    v1 = refs[0].split(":")[1]
    v2 = refs[-1].split(":")[1]
    return f"{book} {ch}:{v1}-{v2}"


def resolve(quoted: str, book: str, refpart: str) -> tuple[str, str]:
    cite = f"{book} {refpart}"
    if cite in SPECIAL:
        return SPECIAL[cite]
    refs = expand(book, refpart)
    if not refs:
        return cite, cite
    if norm(quoted) == norm(join_words(refs)):
        return cite, cite
    for n in range(1, len(refs) + 1):
        pref = join_words(refs[:n])
        if norm(quoted) == norm(pref):
            lookup = refs[0] if n == 1 else lookup_range(book, refs[:n])
            return lookup, cite
    for n in range(1, len(refs) + 1):
        pref = join_words(refs[:n])
        if norm(quoted) in norm(pref):
            lookup = refs[0] if n == 1 else lookup_range(book, refs[:n])
            return lookup, cite
    if len(refs) == 1:
        return refs[0], cite
    return cite, cite


def shortcode_line(lookup: str, cite: str) -> str:
    if lookup == cite:
        return f'  {{{{< jesus-words "{lookup}" >}}}}'
    return f'  {{{{< jesus-words ref="{lookup}" label="{cite}" >}}}}'


def fix_broken_shortcodes(text: str) -> str:
    return re.sub(
        r"^(\s*)\{< jesus-words(.+?)>\}\s*$",
        r"\1{{< jesus-words\2>}}",
        text,
        flags=re.M,
    )


def key_concept_span(text: str) -> tuple[int, int] | None:
    m = re.search(r"^key_concept: \|\n", text, re.M)
    if not m:
        return None
    start = m.end()
    end = start
    for line in text[start:].splitlines(keepends=True):
        if line.strip() == "" or line.startswith("  "):
            end += len(line)
        else:
            break
    return start, end


def migrate_key_concept(text: str) -> tuple[str, int]:
    span = key_concept_span(text)
    if not span:
        return text, 0
    start, end = span
    block = text[start:end]
    changed = 0
    new_lines: list[str] = []
    for line in block.splitlines(keepends=True):
        mm = GOSPEL.match(line.rstrip("\n"))
        if not mm:
            new_lines.append(line)
            continue
        lookup, cite = resolve(mm.group(1), mm.group(2), mm.group(3))
        new_lines.append(shortcode_line(lookup, cite) + "\n")
        changed += 1
    if not changed:
        return text, 0
    return text[:start] + "".join(new_lines) + text[end:], changed


def main() -> None:
    total = 0
    for path in sorted(NOTES.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        text = fix_broken_shortcodes(original)
        new_text, n = migrate_key_concept(text)
        if new_text != original:
            path.write_text(new_text, encoding="utf-8")
        if n:
            print(f"updated {path.name} ({n})")
            total += n
    # ponytail: spot-check — ask-seek-knock cites range, peacemakers single verse
    ask = (NOTES / "ask-seek-knock.md").read_text(encoding="utf-8")
    assert 'label="Matthew 7:7-11"' in ask
    assert 'Matthew 6:9-13' in ask
    assert ask.count("{{< jesus-words") >= 2
    assert '{{< jesus-words "Matthew 5:9" >}}' in (NOTES / "peacemakers.md").read_text(encoding="utf-8")
    print(f"Done — {total} verse line(s) migrated")


if __name__ == "__main__":
    main()
