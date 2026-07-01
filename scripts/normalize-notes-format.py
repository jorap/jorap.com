#!/usr/bin/env python3
"""One-shot: normalize note formatting, dedupe relationships, trim examples to two."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
SKIP = {"_index.md"}
MAX_EXAMPLES = 2

REL_PRIORITY = {"contradicts": 0, "extends": 1, "implements": 2, "alternative": 3}

DOMAIN_KEYWORDS: list[tuple[str, ...]] = [
    ("faith", "church", "sermon", "prayer", "gospel", "worship", "scripture", "pastor"),
    ("parenting", "kid", "child", "son", "daughter", "bedtime", "parent", "father"),
    ("sports", "coach", "ref", "game", "court", "gym", "drill", "whistle", "player"),
    ("digital", "post", "send", "inbox", "email", "slack", "social", "thumb", "tweet"),
    ("healthcare", "clinic", "doctor", "patient", "nurse", "hospital"),
    ("commute", "jeepney", "traffic", "commute", "bus", "pickup line"),
    ("service", "customer", "shift", "restaurant", "wait time"),
    ("workplace", "meeting", "boss", "coworker", "deadline", "office"),
    ("home", "neighbor", "fridge", "parking", "condo", "yard", "chore"),
    ("school", "teacher", "classroom", "homework", "school"),
    ("safety", "incident", "near-miss", "hazard", "site", "ppe"),
    ("pkm", "note", "wikilink", "garden", "whiteboard", "bulletin board"),
]

CARD_ITEM_RE = re.compile(
    r'^\s+-\s+front:\s+"((?:[^"\\]|\\.)*)"\s*\n\s+back:\s+"((?:[^"\\]|\\.)*)"\s*$',
    re.M,
)

REL_ROW_RE = re.compile(
    r"^\| ([^|]+) \| \[\[([^\]]+)\]\] \| ([^|]+) \|$",
    re.M,
)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    fm = text[3:end].lstrip("\n")
    return fm, text[end + 4 :]


def parse_cards(fm: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in CARD_ITEM_RE.finditer(fm)]


def norm(s: str) -> str:
    s = re.sub(r"\[\[([^\]]+)\]\]", r"LINK", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def is_card_echo(bullet: str, cards: list[tuple[str, str]]) -> bool:
    text = bullet[2:].strip() if bullet.startswith("- ") else bullet.strip()
    ntext = norm(text)
    for front, back in cards:
        nfront, nback = norm(front), norm(back)
        combo = f"{nfront} - {nback}"
        if ntext == combo:
            return True
        # front - back pasted with minor punctuation tweaks
        if nfront in ntext and ntext.endswith(nback) and len(ntext) < len(combo) + 30:
            return True
        if ntext.startswith(nfront[: min(40, len(nfront))]) and nback in ntext:
            if len(ntext) < len(nfront) + len(nback) + 25:
                return True
    return False


def bullet_domains(text: str) -> set[str]:
    lower = text.lower()
    found = {row[0] for row in DOMAIN_KEYWORDS if any(k in lower for k in row[1:])}
    return found or {"general"}


def domain_distance(a: set[str], b: set[str]) -> int:
    return len(a ^ b)


def pick_diverse_two(bullets: list[str]) -> list[str]:
    if len(bullets) <= MAX_EXAMPLES:
        return bullets
    domains = [bullet_domains(b) for b in bullets]
    first = 0
    best_j = 1
    best_dist = domain_distance(domains[first], domains[1])
    for j in range(2, len(bullets)):
        dist = domain_distance(domains[first], domains[j])
        if dist > best_dist:
            best_dist = dist
            best_j = j
    return [bullets[first], bullets[best_j]]


def split_section(body: str, heading: str) -> tuple[str, str, str]:
    before, rest = body.split(heading, 1)
    if "##" in rest:
        block, after = rest.split("##", 1)
        after = "##" + after
    else:
        block, after = rest, ""
    return before, block, after


def dedupe_examples(body: str, cards: list[tuple[str, str]]) -> tuple[str, int]:
    if "## Examples" not in body:
        return body, 0
    before, examples_block, after = split_section(body, "## Examples")

    bullets: list[str] = []
    removed = 0
    seen: set[str] = set()

    for line in examples_block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        key = norm(stripped)
        if key in seen:
            removed += 1
            continue
        if cards and is_card_echo(stripped, cards):
            removed += 1
            continue
        seen.add(key)
        bullets.append(stripped)

    trimmed = pick_diverse_two(bullets)
    removed += max(0, len(bullets) - len(trimmed))

    new_block = "\n\n" + "\n".join(trimmed) + "\n\n"
    return before + "## Examples" + new_block + after, removed


def dedupe_relationships(body: str) -> tuple[str, int]:
    if "## Note Relationships" not in body:
        return body, 0
    before, rel_block, after = split_section(body, "## Note Relationships")

    header = "| Relationship | Wikilink | Reason |\n|--------------|----------|--------|"
    if header not in rel_block:
        return body, 0

    best: dict[str, tuple[str, str, str]] = {}
    removed = 0
    for rel, link, reason in REL_ROW_RE.findall(rel_block):
        rel = rel.strip()
        link_key = link.strip().lower()
        reason = reason.strip()
        row = (rel, link.strip(), reason)
        if link_key not in best:
            best[link_key] = row
            continue
        removed += 1
        old_rel, old_link, old_reason = best[link_key]
        old_pri = REL_PRIORITY.get(old_rel, 99)
        new_pri = REL_PRIORITY.get(rel, 99)
        if new_pri < old_pri or (new_pri == old_pri and len(reason) > len(old_reason)):
            best[link_key] = row

    rows = sorted(best.values(), key=lambda r: (r[0].lower(), r[1].lower()))
    table = header + "\n" + "\n".join(f"| {rel} | [[{link}]] | {reason} |" for rel, link, reason in rows)
    new_block = "\n\n" + table + "\n\n"
    return before + "## Note Relationships" + new_block + after, removed


def normalize_file(path: Path, dry_run: bool = False) -> list[str]:
    changes: list[str] = []
    raw = path.read_text(encoding="utf-8")
    fixed = raw.replace("\u2014", "-").replace("\u2013", "-")

    fm, body = split_frontmatter(fixed)
    if not fm:
        if not fixed.endswith("\n"):
            fixed += "\n"
            changes.append("trailing newline")
        if fixed != raw and not dry_run:
            path.write_text(fixed, encoding="utf-8")
        return changes

    cards = parse_cards(fm)

    # No blank line inside frontmatter after opening ---
    if fm.startswith("\n"):
        fm = fm.lstrip("\n")
        changes.append("frontmatter leading blank")

    # Exactly one blank line between closing --- and body
    body = body.lstrip("\n")
    if body:
        body = "\n" + body

    new_body, removed = dedupe_examples(body, cards)
    if removed:
        changes.append(f"trimmed {removed} example(s)")

    new_body, rel_removed = dedupe_relationships(new_body)
    if rel_removed:
        changes.append(f"removed {rel_removed} duplicate relationship(s)")

    out = f"---\n{fm}\n---{new_body}"
    if not out.endswith("\n"):
        out += "\n"
        changes.append("trailing newline")

    if out != raw:
        if not dry_run:
            path.write_text(out, encoding="utf-8")
        if not changes:
            changes.append("format normalized")
    return changes


def verify_notes() -> int:
    """ponytail: one runnable check — fails if duplicates or >2 examples remain."""
    bad = 0
    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        if "## Examples" in text:
            m = re.search(r"## Examples\n\n((?:- .+\n)+)", text)
            if m:
                bullets = [l for l in m.group(1).strip().split("\n") if l.startswith("- ")]
                if len(bullets) > MAX_EXAMPLES:
                    print(f"FAIL examples {path.name}: {len(bullets)}")
                    bad += 1
        if "## Note Relationships" in text:
            rel = text[text.index("## Note Relationships") :]
            rows = [(rel.strip(), link.strip()) for rel, link, _ in REL_ROW_RE.findall(rel)]
            sorted_rows = sorted(rows, key=lambda r: (r[0].lower(), r[1].lower()))
            if rows != sorted_rows:
                print(f"FAIL unsorted rel {path.name}")
                bad += 1
            seen: set[str] = set()
            for _, link, _reason in REL_ROW_RE.findall(rel):
                key = link.strip().lower()
                if key in seen:
                    print(f"FAIL duplicate rel {path.name}: [[{link}]]")
                    bad += 1
                seen.add(key)
    return bad


def main() -> int:
    if "--verify" in sys.argv:
        return 1 if verify_notes() else 0

    dry_run = "--check" in sys.argv
    total_changes = 0
    touched = 0

    for path in sorted(NOTES.glob("*.md")):
        if path.name in SKIP:
            continue
        changes = normalize_file(path, dry_run=dry_run)
        if changes:
            touched += 1
            total_changes += len(changes)
            print(f"{'[check] ' if dry_run else ''}{path.name}: {', '.join(changes)}")

    mode = "would update" if dry_run else "updated"
    print(f"\n{mode} {touched} files ({total_changes} fixes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
