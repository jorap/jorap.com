#!/usr/bin/env python3
"""Rewrite note bodies to atomic form: one claim, short prose, wikilinks — no blog sections."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
SKIP = {"_index", "graph", "maps-of-content", "getting-started", "atomic-notes"}
SEE_ALSO = "## See also"


def split_frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---"):
        return "", text, text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, text
    return text[: end + 4], text[3:end].strip(), text[end + 4 :].lstrip("\n")


def parse_scalar(block: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*"?([^"\n]+)"?', block, re.M)
    return match.group(1).strip() if match else ""


def parse_yaml_list(block: str, key: str) -> list[str]:
    match = re.search(rf"^{key}:\s*\[(.*)\]\s*$", block, re.M)
    if not match:
        return []
    return [item.strip().strip('"') for item in match.group(1).split(",") if item.strip()]


def tag_relatedness(tags_a: list[str], tags_b: list[str]) -> float:
    a, b = set(tags_a), set(tags_b)
    if not a or not b:
        return 0.0
    overlap = len(a & b)
    return 0.0 if overlap == 0 else overlap / min(len(a), len(b))


def build_see_also(stem: str, tags: list[str], catalog: list[dict]) -> str:
    scored: list[tuple[float, dict]] = []
    for note in catalog:
        if note["stem"] == stem:
            continue
        score = tag_relatedness(tags, note["tags"])
        if score > 0:
            scored.append((score, note))
    scored.sort(key=lambda item: (-item[0], item[1]["title"]))
    lines = [SEE_ALSO, ""]
    for _, note in scored[:5]:
        shared = sorted(set(tags) & set(note["tags"]))[:3]
        if shared:
            lines.append(f"- [[{note['title']}]] — {', '.join(shared)}")
        else:
            lines.append(f"- [[{note['title']}]]")
    return "\n".join(lines) + "\n"


def first_desc_sentence(desc: str) -> str:
    desc = desc.strip().rstrip(".")
    match = re.match(r"^(.+?[.!?])", desc)
    return match.group(1).rstrip(".") if match else desc


def lead_text(desc: str) -> str:
    if not desc:
        return desc
    first_word = desc.split()[0] if desc.split() else ""
    if first_word.isupper() and len(first_word) > 1:
        return desc
    if desc[0].isalpha() and desc[0] != "I":
        return desc[0].lower() + desc[1:]
    return desc


def atomize_body(title: str, description: str) -> str:
    desc = description.strip()
    if not desc:
        return f"**{title}**."
    if desc.lower().startswith(title.lower()):
        sentence = f"**{title}**{desc[len(title) :]}"
    else:
        sentence = f"**{title}** — {lead_text(desc)}"
    sentence = sentence.rstrip(".") + "."
    return re.sub(r"\?\.", ".", sentence)


def load_catalog() -> list[dict]:
    catalog = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP | {"_index"}:
            continue
        text = path.read_text(encoding="utf-8")
        _, inner, _ = split_frontmatter(text)
        catalog.append(
            {
                "path": path,
                "stem": path.stem,
                "title": parse_scalar(inner, "title"),
                "tags": parse_yaml_list(inner, "tags"),
                "description": parse_scalar(inner, "description"),
            }
        )
    return catalog


def main() -> None:
    catalog = load_catalog()
    for note in catalog:
        scored = []
        for n in catalog:
            if n["stem"] == note["stem"]:
                continue
            score = tag_relatedness(note["tags"], n["tags"])
            if score > 0:
                scored.append((score, n))
        scored.sort(key=lambda item: (-item[0], item[1]["title"]))
        atomic = atomize_body(note["title"], note["description"])
        see_also = build_see_also(note["stem"], note["tags"], catalog)
        fm, _, _ = split_frontmatter(note["path"].read_text(encoding="utf-8"))
        note["path"].write_text(f"{fm}\n\n{atomic}\n\n{see_also}", encoding="utf-8")
        print(f"atomized: {note['path'].name}")

    print(f"\nDone: {len(catalog)} notes atomized.")


if __name__ == "__main__":
    main()
