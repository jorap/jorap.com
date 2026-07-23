#!/usr/bin/env python3
"""Apply wider Level 1-5 bullets to garden notes from JSON batch data."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from notes_content import split_frontmatter  # noqa: E402


def parse_bullets(kc: str) -> list[str]:
    return [ln.strip()[2:] for ln in kc.splitlines() if ln.strip().startswith("- ")]


def is_level_line(text: str) -> bool:
    return bool(re.match(r"^Level [1-5]: ", text))


def rebuild_key_concept(raw_fm: str, b1: str, levels: list[str], rest: list[str]) -> str:
    match = re.search(r"^(key_concept:\s*\|\s*\n)((?:  .*\n?)*)", raw_fm, re.M)
    if not match:
        raise ValueError("key_concept block not found")

    prefix = match.group(1)
    old_block = match.group(2)
    lines = old_block.splitlines()

    new_lines: list[str] = []
    seen_first_bullet = False
    skipping_levels = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("- "):
            new_lines.append(line)
            continue

        text = stripped[2:]
        if not seen_first_bullet:
            new_lines.append(f"  - {b1}")
            seen_first_bullet = True
            skipping_levels = True
            for lvl in levels:
                new_lines.append(f"  - {lvl}")
            for r in rest:
                new_lines.append(f"  - {r}")
            continue

        if skipping_levels:
            if is_level_line(text):
                continue
            skipping_levels = False

        if is_level_line(text):
            continue

        if text == b1:
            continue

        if text in rest:
            continue

        new_lines.append(line)

    new_block = "\n".join(new_lines)
    if not new_block.endswith("\n"):
        new_block += "\n"

    return raw_fm[: match.start(2)] + new_block + raw_fm[match.end(2) :]


def apply_batch(batch_path: Path) -> tuple[int, list[str]]:
    data = json.loads(batch_path.read_text())
    edited = 0
    skipped: list[str] = []

    for entry in data:
        slug = entry["slug"]
        path = ROOT / "content" / "english" / "notes" / f"{slug}.md"
        if not path.exists():
            skipped.append(f"{slug}: missing file")
            continue

        text = path.read_text()
        raw_fm, body = split_frontmatter(text)
        if not raw_fm:
            skipped.append(f"{slug}: no frontmatter")
            continue

        try:
            new_raw = rebuild_key_concept(raw_fm, entry["b1"], entry["levels"], entry["rest"])
        except ValueError as exc:
            skipped.append(f"{slug}: {exc}")
            continue

        path.write_text(f"---\n{new_raw}\n---\n{body}")
        edited += 1

    return edited, skipped


def main() -> None:
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    path = ROOT / "data" / f"wider-levels-batch-{batch}.json"
    edited, skipped = apply_batch(path)
    print(f"edited: {edited}")
    if skipped:
        print("skipped:")
        for line in skipped:
            print(f"  {line}")


if __name__ == "__main__":
    main()
