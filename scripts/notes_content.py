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
    "shareable_lines",
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
        if key == "shareable_lines" and isinstance(value, list):
            if not value:
                return
            lines.append("shareable_lines:")
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
