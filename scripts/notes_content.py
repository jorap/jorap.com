#!/usr/bin/env python3
"""Shared note body/frontmatter helpers for garden notes."""

from __future__ import annotations

import re
from typing import Any

FM_ORDER = (
    "note_kind",
    "layout",
    "title",
    "meta_title",
    "description",
    "key_concept",
    "examples",
    "shareable_thought",
    "relationships",
    "slug",
    "date",
    "image",
    "categories",
    "author",
    "tags",
    "aliases",
    "featured",
    "review",
    "card_sets",
    "cards",
    "draft",
)

ALWAYS_QUOTE = {
    "note_kind",
    "layout",
    "title",
    "meta_title",
    "description",
    "slug",
    "author",
    "image",
    "date",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[3:end].strip(), text[end + 4 :]


def _parse_scalar(block: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', block, re.M)
    return match.group(1).strip() if match else ""


def _parse_block_scalar(block: str, key: str) -> str:
    match = re.search(rf"^{key}:\s*\|\s*\n((?:  .*\n?)*)", block, re.M)
    if not match:
        return _parse_scalar(block, key)
    lines: list[str] = []
    for line in match.group(1).splitlines():
        lines.append(line[2:] if line.startswith("  ") else line)
    return "\n".join(lines).rstrip("\n")


def _parse_string_list(block: str, key: str) -> list[str]:
    inline = re.search(rf"^{key}:\s*\[(.*)\]\s*$", block, re.M)
    if inline:
        return [
            item.strip().strip('"').strip("'")
            for item in inline.group(1).split(",")
            if item.strip()
        ]
    match = re.search(rf"^{key}:\s*\n((?:  - .*\n?)*)", block, re.M)
    if not match:
        return []
    items: list[str] = []
    for line in match.group(1).splitlines():
        item_match = re.match(r'  - "?(.+?)"?\s*$', line)
        if item_match:
            items.append(item_match.group(1))
    return items


def _parse_relationships(block: str) -> list[dict[str, str]]:
    match = re.search(
        r"^relationships:\s*\n((?:  - .*\n(?:    .*\n?)*)*)", block, re.M
    )
    if not match:
        return []
    rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith("  - "):
            if current:
                rows.append(current)
            current = {}
            rest = line[4:].strip()
            if rest.startswith("type:"):
                current["type"] = rest.split(":", 1)[1].strip()
        elif line.startswith("    "):
            key, _, val = line.strip().partition(":")
            current[key.strip()] = val.strip().strip('"')
    if current:
        rows.append(current)
    return rows


def parse_display_fields(raw_fm: str) -> dict[str, Any]:
    """Parse frontmatter fields needed by assemble_markdown (stdlib only)."""
    fm: dict[str, Any] = {}
    for key in ("description", "summary"):
        val = _parse_scalar(raw_fm, key)
        if val:
            fm[key] = val
    key_concept = _parse_block_scalar(raw_fm, "key_concept")
    if key_concept:
        fm["key_concept"] = key_concept
    examples = _parse_string_list(raw_fm, "examples")
    if examples:
        fm["examples"] = examples
    relationships = _parse_relationships(raw_fm)
    if relationships:
        fm["relationships"] = relationships
    return fm


def relationships_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "## Note Relationships",
        "",
        "| Relationship | Wikilink | Reason |",
        "|--------------|----------|--------|",
    ]
    for row in rows:
        lines.append(f"| {row['type']} | {row['wikilink']} | {row['reason']} |")
    return "\n".join(lines)


def assemble_markdown(fm: dict[str, Any], body: str = "") -> str:
    """Rebuild display markdown from frontmatter fields + optional body."""
    parts: list[str] = []
    description = fm.get("description") or fm.get("summary")
    if isinstance(description, str) and description.strip():
        parts.append(description.strip())

    key_concept = fm.get("key_concept")
    if isinstance(key_concept, str) and key_concept.strip():
        parts.append(f"## Key Concept\n\n{key_concept.strip()}")

    examples = fm.get("examples")
    if isinstance(examples, list) and examples:
        bullets = "\n".join(f"- {ex}" for ex in examples if isinstance(ex, str) and ex.strip())
        if bullets:
            parts.append(f"## Examples\n\n{bullets}")

    relationships = fm.get("relationships")
    if isinstance(relationships, list) and relationships:
        rows = [r for r in relationships if isinstance(r, dict)]
        if rows:
            parts.append(relationships_table(rows))

    body = body.strip()
    if body:
        parts.append(body)
    return "\n\n".join(parts) + ("\n" if parts else "")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_scalar(key: str, value: Any) -> str:
    if isinstance(value, bool):
        return f"{key}: {'true' if value else 'false'}"
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return f"{key}: {value}"
    text = str(value)
    if "\n" in text:
        block = text.rstrip("\n").replace("\n", "\n  ")
        return f"{key}: |\n  {block}"
    if key in ALWAYS_QUOTE or re.search(r'[:#\[\]{}&,*!|>\'"%@`]', text) or text in {
        "true",
        "false",
        "null",
        "yes",
        "no",
        "",
    }:
        return f"{key}: {yaml_quote(text)}"
    return f"{key}: {text}"


def dump_frontmatter(fm: dict[str, Any]) -> str:
    lines: list[str] = []
    seen: set[str] = set()

    def emit(key: str, value: Any) -> None:
        if key in seen or value is None:
            return
        seen.add(key)
        if key == "relationships" and isinstance(value, list):
            if not value:
                return
            lines.append("relationships:")
            for row in value:
                if not isinstance(row, dict):
                    continue
                lines.append(f"  - type: {row.get('type', '')}")
                lines.append(f"    wikilink: {yaml_quote(str(row.get('wikilink', '')))}")
                lines.append(f"    reason: {yaml_quote(str(row.get('reason', '')))}")
            return
        if key == "cards" and isinstance(value, list):
            if not value:
                return
            lines.append("cards:")
            for card in value:
                if not isinstance(card, dict):
                    continue
                lines.append(f'  - front: {yaml_quote(str(card.get("front", "")))}')
                lines.append(f'    back: {yaml_quote(str(card.get("back", "")))}')
            return
        if key in {"tags", "categories", "aliases", "card_sets"} and isinstance(value, list):
            if not value:
                return
            quoted = ", ".join(yaml_quote(str(item)) for item in value)
            lines.append(f"{key}: [{quoted}]")
            return
        if key == "examples" and isinstance(value, list):
            if not value:
                return
            lines.append("examples:")
            for ex in value:
                if isinstance(ex, str) and ex.strip():
                    lines.append(f"  - {yaml_quote(ex.strip())}")
            return
        if key == "shareable_thought" and isinstance(value, list):
            if not value:
                return
            lines.append("shareable_thought:")
            for line in value:
                if isinstance(line, str) and line.strip():
                    lines.append(f"  - {yaml_quote(line.strip())}")
            return
        line = yaml_scalar(key, value)
        if line:
            lines.append(line)

    for key in FM_ORDER:
        if key in fm:
            emit(key, fm[key])
    for key in sorted(fm):
        if key not in seen:
            emit(key, fm[key])
    return "\n".join(lines)


WIKILINK_PLAIN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]+)?\]\]")


def normalize_shareable_line(text: str) -> str:
    text = WIKILINK_PLAIN.sub(r"\1", text)
    text = " ".join(text.replace("`", "").replace("*", "").split()).lower().rstrip(".,;:-— ")
    if text.endswith("…"):
        text = text[:-1].rstrip(".,;:-— ")
    return text


def shareable_lines_overlap(a: str, b: str) -> bool:
    """True when one line is the same claim or an obvious fragment of the other."""
    na, nb = normalize_shareable_line(a), normalize_shareable_line(b)
    if not na or not nb:
        return na == nb
    if na == nb:
        return True
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    if len(shorter) < 10:
        return False
    if longer.startswith(shorter) or longer.endswith(shorter):
        return True
    if shorter.endswith("…"):
        stem = shorter[:-1].rstrip(".,;:-— ")
        if stem and (longer.startswith(stem) or stem in longer):
            return True
    return False


def principle_line_pool(fm: dict) -> list[str]:
    """Normalized clauses drawn only from description and key_concept."""
    pool: list[str] = []
    seen: set[str] = set()
    for field in ("description", "key_concept"):
        src = fm.get(field)
        if not isinstance(src, str) or not src.strip():
            continue
        chunks = [src.strip()]
        for block in src.strip().split("\n\n"):
            block = block.strip()
            if block and "|" not in block:
                chunks.append(block.replace("\n", " "))
        for chunk in chunks:
            flat = WIKILINK_PLAIN.sub(r"\1", chunk)
            flat = " ".join(flat.replace("**", "").replace("*", "").replace("`", "").split())
            parts = [flat]
            parts.extend(re.split(r"(?<=[.!?])\s+|\s[-—–]\s|;\s+", flat))
            for part in parts:
                norm = normalize_shareable_line(part)
                if len(norm) >= 10 and norm not in seen:
                    seen.add(norm)
                    pool.append(norm)
    return pool


FRAGMENT_START = re.compile(
    r"^(not|and|or|but|then)\s",
    re.I,
)
SAME_AS_FRAGMENT = re.compile(r"^same as\b", re.I)
INCOMPLETE_SPLIT_HEAD = re.compile(
    r"\b(isn't|aren't|wasn't|weren't|don't|doesn't|didn't|can't|won't|not merely|not just|not only)\b",
    re.I,
)
POINTER_PREFIX = re.compile(
    r"^(Garden parallel|Same shape|Same rhythm|Same logic|Same math|Same fruit|Same rescue|Faith parallel|More on|Cousins,?|Listed below|Use Note Title|The \[|Goes further than|Pairs with|Ancestor of|See [A-Z]|On [A-Z][a-z]+ [A-Z])\b",
    re.I,
)
META_NOTE_LANG = re.compile(
    r"\b(this note|teach the note|where the note|stage the note|note garden|when a note is only)\b",
    re.I,
)
DANGLING_THAT_START = re.compile(r"^That's\b", re.I)
CLAUSE_SO_START = re.compile(r"^So \b", re.I)
DANGLING_DEMONSTRATIVE = re.compile(r"^that('s| is)\s+the\s+bar\b", re.I)
PUNCH_VERB = re.compile(
    r"\b(kill|kills|win|wins|work|works|beat|beats|need|needs|ship|ships|save|saves|fix|fixes|stop|stops|break|breaks|trust|trusts|keep|keeps|make|makes|go|goes|teach|teaches|name|names|run|runs|build|builds|grow|grows|learn|learns|cite|cites|push|pushes|protect|protects|catch|catches|judge|judges|pick|picks|turn|turns|believe|believes|receive|receives|live|lives|love|loves)\b",
    re.I,
)


def ensure_terminal_punct(text: str) -> str:
    text = text.strip()
    if text and text[-1] not in ".!?":
        text += "."
    return text


def _looks_like_title_fragment(text: str) -> bool:
    """Short title-case phrase without a verb — usually a wikilink label, not a principle."""
    t = text.strip().rstrip(".!?")
    if len(t) > 60 or "," in t or ";" in t:
        return False
    words = t.split()
    if len(words) > 7:
        return False
    return not any(w.islower() for w in words if w.isalpha())


def is_complete_shareable_line(line: str) -> bool:
    """True when line reads as a standalone principle, not a clause fragment."""
    text = line.strip()
    if len(text) < 12:
        return False
    if text.endswith("…"):
        return False
    if text[-1] not in ".!?":
        return False
    if text.endswith((",", ";", " -", "—", "–")):
        return False
    if not (text[0].isupper() or text[0] in '"\'('):
        return False
    if FRAGMENT_START.match(text):
        return False
    if SAME_AS_FRAGMENT.match(text):
        return False
    if text.count("(") > text.count(")"):
        return False
    if _looks_like_title_fragment(text):
        return False
    return True


def _incomplete_negation_line(text: str) -> bool:
    """Negation-only line that needs its contrast half to land."""
    if len(text) > 90:
        return False
    lower = text.lower()
    if not any(
        x in lower
        for x in ("isn't", "aren't", "don't", "doesn't", "not merely", "not just", "not only")
    ):
        return False
    if " - " in text or "; " in text:
        return False
    if ", not " in lower:
        return False
    if lower.startswith("the point isn't"):
        return True
    if "don't hand back" in lower:
        return True
    return False


def _bare_noun_list(text: str) -> bool:
    """Comma list of labels with no verb - e.g. 'Judgment, patience, attention.'"""
    t = text.rstrip(".!?").strip()
    if "," not in t or " - " in t or " not " in t.lower():
        return False
    if PUNCH_VERB.search(t):
        return False
    parts = [p.strip() for p in t.split(",")]
    return len(parts) >= 2 and all(len(p.split()) <= 2 for p in parts)


def gets_point_across(line: str) -> bool:
    """True when a reader gets the claim without another line for context."""
    if not is_complete_shareable_line(line):
        return False
    text = line.strip()
    words = text.split()
    if len(words) < 5 and len(text) < 35 and not PUNCH_VERB.search(text):
        return False
    if POINTER_PREFIX.match(text):
        return False
    if META_NOTE_LANG.search(text):
        return False
    if DANGLING_THAT_START.match(text):
        return False
    if CLAUSE_SO_START.match(text):
        return False
    if DANGLING_DEMONSTRATIVE.match(text):
        return False
    if _bare_noun_list(text):
        return False
    if "listed below" in text.lower():
        return False
    if re.match(r"^In that order\.?$", text, re.I):
        return False
    if re.search(r"\[.*\]\([^)]+\)", text):
        return False
    if text.startswith("For ") and not PUNCH_VERB.search(text):
        return False
    if _incomplete_negation_line(text):
        return False
    return True


def _self_check() -> None:
    assert is_complete_shareable_line("Friction kills capture.")
    assert is_complete_shareable_line("Same aim, different plan.")
    assert not is_complete_shareable_line("not mere intellectual agreement.")
    assert not is_complete_shareable_line("Same as The Trusted Inbox.")
    assert not is_complete_shareable_line("There Is No Perfect Solution")
    assert not gets_point_across("The point isn't passivity toward all evil.")
    assert not gets_point_across("Same inbox rule.")
    assert not gets_point_across("That's the pushback on busy-as-virtue.")
    assert not gets_point_across("See The Narrow Way and Loss of Reward for false profession.")
    assert not gets_point_across("Integrity in general; this note is the team-visible lane.")
    assert not gets_point_across("So you change the process, not only patch today's fire.")
    assert gets_point_across("Friction kills capture.")
    assert gets_point_across("The point isn't passivity toward all evil - it's refusing to become what hurt you.")
    assert ensure_terminal_punct("Keep the goal") == "Keep the goal."


def shareable_line_from_principle(line: str, fm: dict) -> bool:
    """True when line is a clause from description or key_concept, not meta padding."""
    nl = normalize_shareable_line(line)
    if not nl:
        return False
    for p in principle_line_pool(fm):
        if nl == p:
            return True
        if len(nl) >= 10 and (p.startswith(nl) or nl.startswith(p) or nl in p or p in nl):
            return True
    return False
