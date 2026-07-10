#!/usr/bin/env python3
"""Apply mechanical garden-voice fixes without re-serializing YAML frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml required")

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "content/english/notes"
DESC_DATA = ROOT / "data/garden-voice-descriptions.yaml"
FM = re.compile(r"^(---\s*\n)(.*?)(\n---)", re.DOTALL)
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
SKIP_KINDS = frozenset({"meta", "index"})
SKIP_FILES = frozenset({"_index.md"})

CONTRACTIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bI'm\b"), "I am"),
    (re.compile(r"\bI've\b"), "I have"),
    (re.compile(r"\bI'll\b"), "I will"),
    (re.compile(r"\bI'd\b"), "I would"),
    (re.compile(r"\bthey're\b", re.I), "they are"),
    (re.compile(r"\bwe're\b", re.I), "we are"),
    (re.compile(r"\byou're\b", re.I), "you are"),
    (re.compile(r"\bwe'll\b", re.I), "we will"),
    (re.compile(r"\byou'll\b", re.I), "you will"),
    (re.compile(r"\bthey'll\b", re.I), "they will"),
    (re.compile(r"\bwe'd\b", re.I), "we would"),
    (re.compile(r"\byou'd\b", re.I), "you would"),
    (re.compile(r"\bthey'd\b", re.I), "they would"),
    (re.compile(r"\bwho'd\b", re.I), "who would"),
    (re.compile(r"\bwho'll\b", re.I), "who will"),
    (re.compile(r"\byou've\b", re.I), "you have"),
    (re.compile(r"\bthey've\b", re.I), "they have"),
    (re.compile(r"\bwe've\b", re.I), "we have"),
    (re.compile(r"\bcould've\b", re.I), "could have"),
    (re.compile(r"\bwould've\b", re.I), "would have"),
    (re.compile(r"\bshould've\b", re.I), "should have"),
    (re.compile(r"\bshe'd\b", re.I), "she would"),
    (re.compile(r"\bhe'd\b", re.I), "he would"),
    (re.compile(r"\bdon't\b", re.I), "do not"),
    (re.compile(r"\bdoesn't\b", re.I), "does not"),
    (re.compile(r"\bdidn't\b", re.I), "did not"),
    (re.compile(r"\bwon't\b", re.I), "will not"),
    (re.compile(r"\bcan't\b", re.I), "cannot"),
    (re.compile(r"\bisn't\b", re.I), "is not"),
    (re.compile(r"\baren't\b", re.I), "are not"),
    (re.compile(r"\bwasn't\b", re.I), "was not"),
    (re.compile(r"\bweren't\b", re.I), "were not"),
    (re.compile(r"\bhaven't\b", re.I), "have not"),
    (re.compile(r"\bhasn't\b", re.I), "has not"),
    (re.compile(r"\bhadn't\b", re.I), "had not"),
    (re.compile(r"\bwouldn't\b", re.I), "would not"),
    (re.compile(r"\bcouldn't\b", re.I), "could not"),
    (re.compile(r"\bshouldn't\b", re.I), "should not"),
    (re.compile(r"\bit's\b"), "it is"),
    (re.compile(r"\bthat's\b"), "that is"),
    (re.compile(r"\bthere's\b"), "there is"),
    (re.compile(r"\blet's\b"), "let us"),
]


def load_descriptions() -> dict[str, str]:
    if not DESC_DATA.is_file():
        return {}
    raw = yaml.safe_load(DESC_DATA.read_text(encoding="utf-8")) or {}
    return {str(k): str(v) for k, v in (raw.get("descriptions") or {}).items()}


def decontract(text: str) -> str:
    out = text
    for pattern, repl in CONTRACTIONS:
        out = pattern.sub(repl, out)
    return out


def strip_wikilinks(text: str) -> str:
    return WIKILINK.sub(lambda m: m.group(1).strip(), text)


def first_sentence(text: str) -> str:
    text = text.strip()
    match = re.search(r"^(.*?[.!?])(?:\s+|$)", text)
    return match.group(1).strip() if match else text


def rebullet_key_concept(block: str) -> str:
    out_lines = []
    for line in block.splitlines(keepends=True):
        stripped = line.strip()
        if not stripped:
            out_lines.append(line)
            continue
        if stripped.startswith("{{<") or stripped.startswith("- "):
            out_lines.append(line)
            continue
        indent = line[: len(line) - len(line.lstrip())]
        suffix = "\n" if line.endswith("\n") else ""
        out_lines.append(f"{indent}- {stripped}{suffix}")
    return "".join(out_lines)


def fix_key_concept_block(block: str) -> str:
    block = rebullet_key_concept(block)
    lines = block.splitlines(keepends=True)
    idx = None
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("{{"):
            continue
        if line.startswith("- "):
            idx = i
            break
        idx = i
        break
    if idx is None:
        return decontract(block)
    raw = lines[idx]
    stripped = raw.strip()
    if stripped.startswith("- "):
        body = stripped[2:]
        if WIKILINK.search(body):
            new_body = strip_wikilinks(body)
            lines[idx] = raw.replace(body, new_body, 1)
    elif WIKILINK.search(stripped):
        lines[idx] = strip_wikilinks(raw)
    return decontract("".join(lines))


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def replace_description(fm: str, new_desc: str) -> str:
    quoted = yaml_quote(new_desc)
    if re.search(r"^description:\s*.+$", fm, re.M):
        return re.sub(r"^description:\s*.+$", f"description: {quoted}", fm, count=1, flags=re.M)
    return fm


def extract_block(fm: str, field: str) -> tuple[int, int, str] | None:
    """Return start, end, body for `field: |` block inside frontmatter."""
    header = re.search(rf"^{field}: \|\n", fm, re.M)
    if not header:
        return None
    start = header.end()
    tail = fm[start:]
    next_key = re.search(r"^[a-z_][a-z0-9_]*:", tail, re.M)
    end = start + (next_key.start() if next_key else len(tail))
    return start, end, fm[start:end]


def set_block(fm: str, start: int, end: int, new_body: str) -> str:
    return fm[:start] + new_body + fm[end:]


def replace_pipe_field(fm: str, field: str, transform) -> str:
    found = extract_block(fm, field)
    if not found:
        return fm
    start, end, block = found
    new_block = transform(block)
    if new_block == block:
        return fm
    return set_block(fm, start, end, new_block)


def extract_list_block(fm: str, field: str) -> tuple[int, int, str] | None:
    header = re.search(rf"^{field}:\n", fm, re.M)
    if not header:
        return None
    start = header.end()
    tail = fm[start:]
    next_key = re.search(r"^[a-z_][a-z0-9_]*:", tail, re.M)
    end = start + (next_key.start() if next_key else len(tail))
    return start, end, fm[start:end]


def replace_list_field(fm: str, field: str, transform) -> str:
    found = extract_list_block(fm, field)
    if not found:
        return fm
    start, end, block = found
    new_block = transform(block)
    if new_block == block:
        return fm
    return set_block(fm, start, end, new_block)


def transform_list_block(block: str) -> str:
    out_lines = []
    for line in block.splitlines(keepends=True):
        m = re.match(r"^(  - )(.+?)(\r?\n)?$", line)
        if not m:
            out_lines.append(line)
            continue
        prefix, body, ending = m.group(1), m.group(2), m.group(3) or ""
        if body.startswith('"') and body.endswith('"'):
            inner = body[1:-1].replace('\\"', '"')
            inner = decontract(first_sentence(inner))
            body = yaml_quote(inner)
        else:
            body = decontract(first_sentence(body))
        out_lines.append(prefix + body + ending)
    return "".join(out_lines)


def transform_shareable_block(block: str) -> str:
    out_lines = []
    for line in block.splitlines(keepends=True):
        m = re.match(r"^(  - )(.+?)(\r?\n)?$", line)
        if not m:
            out_lines.append(line)
            continue
        prefix, body, ending = m.group(1), m.group(2), m.group(3) or ""
        if body.startswith('"') and body.endswith('"'):
            inner = body[1:-1].replace('\\"', '"')
            inner = decontract(inner)
            body = yaml_quote(inner)
        else:
            body = decontract(body)
        out_lines.append(prefix + body + ending)
    return "".join(out_lines)


def transform_reasons(fm: str) -> str:
    out_lines = []
    for line in fm.splitlines(keepends=True):
        m = re.match(r"^(\s+reason: )(.+?)(\r?\n)?$", line)
        if not m:
            out_lines.append(line)
            continue
        prefix, body, ending = m.group(1), m.group(2).strip(), m.group(3) or ""
        if body.startswith('"') and body.endswith('"'):
            inner = decontract(body[1:-1].replace('\\"', '"'))
            body = yaml_quote(inner)
        else:
            body = decontract(body.strip("\"'"))
        out_lines.append(prefix + body + ending)
    return "".join(out_lines)


def migrate_file(path: Path, descriptions: dict[str, str], *, dry_run: bool) -> str | None:
    if path.name in SKIP_FILES:
        return None
    text = path.read_text(encoding="utf-8")
    match = FM.match(text)
    if not match:
        return None
    fm_open, fm, fm_close = match.group(1), match.group(2), match.group(3)
    meta = yaml.safe_load(fm) or {}
    if meta.get("draft") or meta.get("note_kind", "note") in SKIP_KINDS:
        return None

    original_fm = fm
    slug = path.stem

    if slug in descriptions:
        fm = replace_description(fm, descriptions[slug])

    fm = replace_pipe_field(fm, "key_concept", fix_key_concept_block)
    fm = replace_list_field(fm, "examples", transform_list_block)
    fm = replace_list_field(fm, "shareable_thought", transform_shareable_block)
    fm = transform_reasons(fm)

    if fm == original_fm:
        return None

    if dry_run:
        return f"{path.relative_to(ROOT)}: would update"

    body = text[match.end() :]
    path.write_text(fm_open + fm + fm_close + body, encoding="utf-8")
    return f"{path.relative_to(ROOT)}: updated"


def _self_check() -> None:
    assert strip_wikilinks("[[Foo]] bar") == "Foo bar"
    assert decontract("they're") == "they are"
    sample = 'description: "old"\nkey_concept: |\n  - [[Foo]] claim\n'
    out = replace_pipe_field(sample, "key_concept", fix_key_concept_block)
    assert "[[Foo]]" not in out.split("key_concept")[1].split("\n")[1]


def main() -> int:
    if "--self-check" in sys.argv:
        _self_check()
        print("garden-voice-migrate self-check OK")
        return 0

    dry_run = "--dry-run" in sys.argv
    descriptions = load_descriptions()
    logs = []
    for path in sorted(NOTES.glob("*.md")):
        line = migrate_file(path, descriptions, dry_run=dry_run)
        if line:
            logs.append(line)

    for line in logs:
        print(line)
    print(f"\n{'Would update' if dry_run else 'Updated'} {len(logs)} notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
