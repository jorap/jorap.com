#!/usr/bin/env python3
"""Add when-clauses to bare contradicts relationship lines."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"

sys.path.insert(0, str(ROOT / "scripts"))
from contradicts_when import CONTRADICTS_WHEN, ONLY_WHEN_SLUGS  # noqa: E402

HAS_QUALIFIER = re.compile(r"Contradicts \[\[[^\]]+\]\]\s+(?:when|only when|unless)\s+", re.I)
REL_LINE = re.compile(r"^Extends \[\[[^\]]+\]\]\..+$")


def qualify_contradicts(line: str, slug: str) -> str:
    if HAS_QUALIFIER.search(line):
        return line
    when = CONTRADICTS_WHEN.get(slug)
    if not when:
        return line
    prefix = "only when" if slug in ONLY_WHEN_SLUGS else "when"
    return re.sub(
        r"(Contradicts \[\[[^\]]+\]\])\.(\s*)",
        rf"\1 {prefix} {when}.\2",
        line,
        count=1,
    )


def upgrade_body(body: str, slug: str) -> tuple[str, bool]:
    lines = body.splitlines()
    changed = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Extends ") and "Contradicts " in stripped:
            updated = qualify_contradicts(stripped, slug)
            if updated != stripped:
                changed = True
            new_lines.append(updated)
        else:
            new_lines.append(line)
    text = "\n".join(new_lines)
    if body.endswith("\n") and not text.endswith("\n"):
        text += "\n"
    return text, changed


def main() -> int:
    updated = 0
    missing: list[str] = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        slug = path.stem
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        fm, body = text[: end + 4], text[end + 4 :]
        rel = [ln.strip() for ln in body.splitlines() if ln.strip().startswith("Extends ") and "Contradicts " in ln]
        if not rel:
            continue
        if slug not in CONTRADICTS_WHEN and any(not HAS_QUALIFIER.search(ln) for ln in rel):
            missing.append(slug)
            continue
        new_body, changed = upgrade_body(body, slug)
        if changed:
            path.write_text(fm + new_body, encoding="utf-8")
            print(f"  {path.name}")
            updated += 1
    print(f"\nDone: {updated} notes qualified.")
    if missing:
        print(f"Missing when-clause ({len(missing)}): {', '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
