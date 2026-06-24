#!/usr/bin/env python3
"""Replace genre-tagged ## Examples with up to five ranked genre-free bullets."""
import re
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1] / "content/english/notes"


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, text[m.end() :]


def quality(sentence: str) -> int:
    s = sentence.lower()
    q = 0
    if re.search(
        r"\b(thumb|jeepney|receipt|slack|group chat|draft|inbox|clinic|voice-memo|elevator|dinner|bed|midnight|huddle|locker room|voided|deleted my matching)\b",
        sentence,
        re.I,
    ):
        q += 3
    if re.search(r"\b(I |my )", sentence):
        q += 2
    words = len(sentence.split())
    if 15 <= words <= 35:
        q += 2
    if "one owner" in s or "ticket to heaven" in s:
        q -= 3
    if s.startswith("after ") and "named who" in s:
        q -= 3
    if "same posture, different room" in s:
        q -= 2
    if "week ten finally bit" in s and s.startswith("january"):
        q -= 2
    return q


def card_to_example(front: str, back: str) -> str:
    front = front.strip().rstrip("?")
    back = back.strip()
    return f"{front} - {back}"


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())[:80]


def pool_for_note(fm: dict, examples_block: str) -> list[tuple[str, int]]:
    pool: list[tuple[str, int]] = []
    for line in re.findall(r"^- (.+)$", examples_block, re.M):
        if line.startswith("**"):  # legacy genre line if re-run on old file
            _, sentence = re.match(r"^- \*\*[^*]+:\*\* (.+)$", line).groups()
        else:
            sentence = line
        pool.append((sentence.strip(), quality(sentence) + 5))
    for c in fm.get("cards") or []:
        if not isinstance(c, dict):
            continue
        front = c.get("front", "")
        back = c.get("back", "")
        if front and back:
            pool.append((card_to_example(front, back), quality(front) + quality(back)))
    pool.sort(key=lambda x: x[1], reverse=True)
    return pool


def pick_top5(pool: list[tuple[str, int]]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for sentence, _ in pool:
        key = normalize(sentence)
        if key in seen:
            continue
        seen.add(key)
        out.append(sentence)
        if len(out) == 5:
            break
    return out


def format_examples(bullets: list[str]) -> str:
    lines = ["## Examples", ""]
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    return "\n".join(lines) + "\n"


def update_note(path: pathlib.Path) -> bool:
    text = path.read_text()
    fm, _ = parse_frontmatter(text)
    if fm.get("note_kind") in ("index", "meta"):
        return False
    m = re.search(r"^## Examples\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return False
    pool = pool_for_note(fm, m.group(1))
    top = pick_top5(pool)
    if not top:
        return False
    new_block = format_examples(top)
    new_text = text[: m.start()] + new_block + text[m.end() :]
    if new_text == text:
        return False
    path.write_text(new_text)
    return True


def main():
    updated = sum(
        1
        for p in sorted(ROOT.glob("*.md"))
        if not p.name.startswith("_") and update_note(p)
    )
    print(f"updated {updated} notes")


if __name__ == "__main__":
    main()
