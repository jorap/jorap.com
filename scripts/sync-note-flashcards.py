#!/usr/bin/env python3
"""Ensure every garden note has 2/4/6/8 flashcards by importance tier."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from notes_content import assemble_markdown, dump_frontmatter, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"

SKIP_STEMS = {
    "_index",
    "flashcards",
    "review",
    "graph",
    "issues",
    "random-duo",
    "create",
    "okf-export",
}
SKIP_KINDS = {"meta", "index"}
SKIP_LAYOUTS = {"graph", "cards", "review", "issues", "backlinks", "random-duo", "create"}

# Hub + top spine → 8 cards
TIER_EIGHT = {
    "getting-started",
    "eternal-principles",
    "maps-of-content",
    "capture",
    "free-grace",
    "the-golden-rule",
    "seek-the-kingdom-first",
    "pareto-principle",
    "the-trusted-inbox",
    "weekly-review-checklists",
}

# Gospel + core PKM habits (existing review spine) → 6
TIER_SIX_TAGS = {"gospel", "eternal principles", "sermon on the mount"}
TIER_SIX_STEMS = {
    "building-a-second-brain",
    "atomic-notes",
    "linking-by-meaning",
    "evergreen-notes",
    "signal-vs-noise",
    "the-collectors-fallacy",
    "note-relationships",
    "para-method",
    "spaced-repetition",
}

# Safety, workplace, leadership → 4
TIER_FOUR_TAGS = {
    "safety",
    "workplace",
    "coaching",
    "risk management",
    "ethics",
    "leadership",
}

# Hand-tuned spine decks - tier 6/8; only expand/trim count, never replace existing cards
HANDCRAFTED_STEMS = {
    "abide-in-me", "ask-seek-knock", "assurance", "atomic-notes", "linking-by-meaning",
    "building-a-second-brain", "by-their-fruits", "capture", "childlike-faith",
    "christianity-and-politics", "discipleship", "dont-worry", "eternal-rewards",
    "evergreen-notes", "faith-and-works", "faithful-steward", "forgiveness",
    "free-grace", "grateful-obedience", "great-commission", "heart-righteousness",
    "humility-and-service", "judge-not", "judgment-seat", "justification",
    "let-your-light-shine", "let-your-yes-be-yes", "loss-of-reward", "love-god",
    "love-your-enemies", "love-your-neighbor", "note-relationships", "para-method",
    "pareto-principle", "peacemakers", "reconciliation-before-worship",
    "render-unto-caesar", "repent-and-believe", "sanctification", "secret-devotion",
    "seek-the-kingdom-first", "signal-vs-noise", "standing-vs-fellowship",
    "take-up-your-cross", "the-beatitudes", "the-collectors-fallacy", "the-golden-rule",
    "the-narrow-way", "the-trusted-inbox", "the-wise-builder", "treasure-in-heaven",
    "turn-the-other-cheek", "weekly-review-checklists", "wood-hay-stubble",
}

CARD_ITEM_RE = re.compile(
    r'^\s+-\s+front:\s+"((?:[^"\\]|\\.)*)"\s*\n\s+back:\s+"((?:[^"\\]|\\.)*)"\s*$',
    re.M,
)
LEAD_RE = re.compile(r"^\*\*([^*]+)\*\*\s*=\s*(.+)$", re.M)
EXAMPLE_RE = re.compile(r"^-\s+(.+)$", re.M)

# lint: no multiple-choice forks on front
MC_FORK_OR_RE = re.compile(r"\bor\b[^.?!\n]*\?", re.I)


def load_fm(raw_fm: str) -> dict:
    data = yaml.safe_load(raw_fm) or {}
    return data if isinstance(data, dict) else {}


def content_for_cards(raw_fm: str, body: str) -> str:
    fm = load_fm(raw_fm)
    return assemble_markdown(fm, body)


def parse_cards(fm: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in CARD_ITEM_RE.finditer(fm)]


def parse_tags(fm: str) -> list[str]:
    m = re.search(r"^tags:\s*\[(.*)\]\s*$", fm, re.M)
    if not m:
        return []
    return [t.strip().strip('"').lower() for t in m.group(1).split(",") if t.strip()]


def is_garden_note(fm: str, stem: str) -> bool:
    if stem in SKIP_STEMS:
        return False
    kind = re.search(r'^note_kind:\s*"?(\w+)"?', fm, re.M)
    if kind and kind.group(1) in SKIP_KINDS:
        return False
    layout = re.search(r'^layout:\s*"?(\w+)"?', fm, re.M)
    if layout and layout.group(1) in SKIP_LAYOUTS:
        return False
    return True


def target_count(stem: str, fm: str, tags: list[str]) -> int:
    if re.search(r"^featured:\s*true\s*$", fm, re.M) or stem in TIER_EIGHT:
        return 8
    tagset = set(tags)
    if "workplace" in tagset and "gospel" not in tagset:
        return 4
    if tagset & TIER_SIX_TAGS or stem in TIER_SIX_STEMS or stem in HANDCRAFTED_STEMS:
        return 6
    if tagset & TIER_FOUR_TAGS or "leadership" in tagset:
        return 4
    if "pkm" in tagset or "productivity" in tagset or "note taking" in tagset:
        return 4
    return 2


def pick_card_sets(tags: list[str], stem: str) -> list[str]:
    tagset = set(tags)
    if "workplace" in tagset and "gospel" not in tagset:
        return ["Ethics", "Focus"]
    if tagset & TIER_SIX_TAGS or ("eternal principles" in tagset and "gospel" in tagset):
        section = "Faith"
        if "commandments" in tagset or "love god" in stem:
            section = "Commandments"
        elif "ethics" in tagset or "sermon on the mount" in tagset:
            section = "Ethics"
        elif "prayer" in tagset or "devotion" in stem:
            section = "Prayer"
        elif "priorities" in tagset or "kingdom" in stem:
            section = "Priorities"
        elif "discipleship" in tagset or stem in {"great-commission", "discipleship"}:
            section = "Discipleship"
        return ["Eternal Principles", "Gospel", section]
    if tagset & TIER_FOUR_TAGS or "workplace" in tagset:
        return ["Ethics", "Focus"]
    if "capture" in tagset or stem in {"capture", "the-trusted-inbox"}:
        return ["Capture", "Workflow"]
    if "linking" in tagset or "link" in stem:
        return ["Linking", "Review"]
    if "writing" in tagset or "evergreen" in stem:
        return ["Writing", "Review"]
    if "focus" in tagset or "productivity" in tagset:
        return ["Focus", "Workflow"]
    return ["Focus", "Review"]


def compress_back(text: str, max_len: int = 48) -> str:
    text = re.sub(r"\[\[([^\]|]+)\]\]", r"\1", text)
    text = text.strip().rstrip(".")
    # first clause
    for sep in (".", ";", " - ", ","):
        if sep in text:
            text = text.split(sep)[0].strip()
    if len(text) > max_len:
        text = text[: max_len - 3].rsplit(" ", 1)[0] + "..."
    return text


def claim_to_back(claim: str) -> str:
    claim = re.sub(r"\[\[([^\]|]+)\]\]", r"\1", claim).strip().rstrip(".")
    m = re.match(r"if .+?,\s*I\s+(.+)$", claim, re.I)
    if m:
        back = m.group(1).strip()
        if back:
            back = back[0].upper() + back[1:]
            return compress_back(back, 52)
    return compress_back(claim, 52)


def action_to_back(action: str) -> str:
    action = action.strip().rstrip(".")
    if not action:
        return ""
    m = re.search(r"\bI\s+(.+)$", action, re.I)
    if m:
        verb = m.group(1).strip()
        if len(verb) <= 52:
            return verb[0].upper() + verb[1:]
    if len(action) <= 52:
        return action[0].upper() + action[1:]
    for sep in (" - ", ";", ","):
        if sep in action:
            tail = action.split(sep)[-1].strip()
            if 4 < len(tail) <= 52:
                return tail[0].upper() + tail[1:]
    words = action.split()
    if len(words) > 8:
        return " ".join(words[:8]).rstrip(",") + "."
    return compress_back(action, 52)


def example_to_card(line: str, claim: str) -> tuple[str, str] | None:
    text = re.sub(r"\[\[([^\]|]+)\]\]", r"\1", line.strip())
    if not text:
        return None
    scenario, action = text, ""
    if " - " in text:
        scenario, action = text.split(" - ", 1)
        scenario, action = scenario.strip(), action.strip()
    front = scenario
    if len(front) < 55:
        front = f"{scenario}. What's the move?"
    back = action_to_back(action) if action else claim_to_back(claim)
    if not back:
        back = claim_to_back(claim)
    if len(front) <= len(back):
        front = front + " One check?"
    if MC_FORK_OR_RE.search(front):
        front = scenario + ". What's the move?"
    return front, back


def fallback_cards(claim: str, title: str, n: int) -> list[tuple[str, str]]:
    short = claim_to_back(claim) if claim else f"Apply {title.lower()}."
    templates = [
        (
            f"Mid-week moment where {title.lower()} should've fired. What's the move?",
            short,
        ),
        (
            f"Pressure rising and I'm about to skip this principle. One move?",
            short,
        ),
        (
            f"Someone asks why I do it this way. One sentence back?",
            short,
        ),
        (
            f"Old habit pulling the wrong way again. What do I do first?",
            short,
        ),
    ]
    return templates[:n]


def generate_cards(body: str, title: str, need: int) -> list[tuple[str, str]]:
    claim = ""
    m = LEAD_RE.search(body)
    if m:
        claim = m.group(2).strip()

    examples: list[str] = []
    if "## Examples" in body:
        block = body.split("## Examples", 1)[1].split("##", 1)[0]
        seen: set[str] = set()
        for line in block.splitlines():
            em = EXAMPLE_RE.match(line.strip())
            if not em:
                continue
            key = re.sub(r"\s+", " ", em.group(1).lower())[:80]
            if key in seen:
                continue
            seen.add(key)
            examples.append(em.group(1))

    cards: list[tuple[str, str]] = []
    for ex in examples:
        if len(cards) >= need:
            break
        pair = example_to_card(ex, claim or title)
        if pair:
            cards.append(pair)

    if len(cards) < need:
        cards.extend(fallback_cards(claim or title, title, need - len(cards)))

    return cards[:need]


def yaml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def cards_yaml(cards: list[tuple[str, str]]) -> str:
    lines = ["cards:"]
    for front, back in cards:
        lines.append(f'  - front: "{yaml_escape(front)}"')
        lines.append(f'    back: "{yaml_escape(back)}"')
    return "\n".join(lines)


def inject_cards_dict(fm: dict, card_sets: list[str], cards: list[tuple[str, str]]) -> dict:
    fm = dict(fm)
    fm["review"] = True
    fm["card_sets"] = card_sets
    fm["cards"] = [{"front": front, "back": back} for front, back in cards]
    return fm


def sync_file(path: Path, dry_run: bool = False, rewrite: bool = False) -> str | None:
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)
    if not raw_fm:
        return None
    fm = load_fm(raw_fm)
    stem = path.stem
    if not is_garden_note(raw_fm, stem):
        return None

    tags = parse_tags(raw_fm)
    target = target_count(stem, raw_fm, tags)
    existing = parse_cards(raw_fm)

    title = str(fm.get("title") or stem.replace("-", " ").title())
    assembled = content_for_cards(raw_fm, body)

    if len(existing) == target and not rewrite:
        return None

    if stem in HANDCRAFTED_STEMS and existing:
        if rewrite:
            return None
        if len(existing) > target:
            cards = existing[:target]
            action = f"trim {len(existing)}→{target}"
        elif len(existing) < target:
            extra = generate_cards(assembled, title, target - len(existing))
            cards = existing + extra
            action = f"expand {len(existing)}→{target}"
        else:
            if len(existing) == target:
                return None
            cards = existing
            action = "fix frontmatter"
    elif rewrite or not existing:
        cards = generate_cards(assembled, title, target)
        action = f"rewrite {len(cards)} cards (tier {target})"
    elif len(existing) > target:
        cards = existing[:target]
        action = f"trim {len(existing)}→{target}"
    elif len(existing) < target:
        cards = existing + generate_cards(body, title, target - len(existing))
        action = f"expand {len(existing)}→{target}"
    else:
        cards = generate_cards(assembled, title, target)
        action = f"add {len(cards)} cards (tier {target})"

    card_sets = pick_card_sets(tags, stem)
    fm = inject_cards_dict(fm, card_sets, cards)
    new_text = f"---\n{dump_frontmatter(fm)}\n---\n{body.lstrip(chr(10))}"
    if not new_text.endswith("\n"):
        new_text += "\n"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return f"{path.name}: {action}"


def main() -> int:
    dry_run = "--check" in sys.argv
    rewrite = "--rewrite" in sys.argv
    changes: list[str] = []
    for path in sorted(NOTES.glob("*.md")):
        msg = sync_file(path, dry_run=dry_run, rewrite=rewrite)
        if msg:
            changes.append(msg)

    prefix = "[check] " if dry_run else ""
    for c in changes:
        print(f"{prefix}{c}")
    print(f"\n{'would update' if dry_run else 'updated'} {len(changes)} notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
