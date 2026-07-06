#!/usr/bin/env python3
"""Export the published notes garden to an OKF v0.1 bundle."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from notes_content import (
    assemble_markdown,
    parse_bool,
    parse_display_fields,
    parse_scalar,
    split_frontmatter_parts as split_frontmatter,
)

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "content/english/notes"
HUGO_TOML = ROOT / "hugo.toml"
DEFAULT_OUT = ROOT / "static/exports/okf"
OKF_VERSION = "0.1"
SKIP_STEMS = {"_index"}
UTILITY_LAYOUTS = frozenset(
    {"graph", "cards", "review", "issues", "random-duo", "create", "backlinks"}
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?\]\]")
BASEURL_RE = re.compile(r'^baseURL\s*=\s*"([^"]+)"', re.M)


@dataclass(frozen=True)
class NoteRecord:
    path: Path
    slug: str
    title: str
    description: str
    tags: list[str]
    note_kind: str
    draft: bool
    utility: bool
    timestamp: str
    resource: str


def parse_yaml_list(block: str, key: str) -> list[str]:
    match = re.search(rf"^{key}:\s*\[(.*)\]\s*$", block, re.M)
    if not match:
        return []
    return [item.strip().strip('"') for item in match.group(1).split(",") if item.strip()]


def slugify(value: str) -> str:
    value = value.casefold().strip()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def read_base_url() -> str:
    if not HUGO_TOML.exists():
        return "https://www.jorap.com/"
    text = HUGO_TOML.read_text(encoding="utf-8")
    match = BASEURL_RE.search(text)
    if not match:
        return "https://www.jorap.com/"
    return match.group(1).rstrip("/") + "/"


def is_utility(block: str) -> bool:
    if parse_scalar(block, "note_kind") == "meta":
        return True
    return parse_scalar(block, "layout") in UTILITY_LAYOUTS


def note_timestamp(inner: str, path: Path) -> str:
    raw = parse_scalar(inner, "date")
    if raw:
        try:
            if raw.endswith("Z"):
                dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            else:
                dt = datetime.fromisoformat(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def body_without_see_also(body: str) -> str:
    if "## See also" not in body:
        return body
    return body.split("## See also", 1)[0].rstrip() + "\n"


def load_notes(base_url: str) -> tuple[list[NoteRecord], dict[str, NoteRecord]]:
    records: list[NoteRecord] = []
    by_key: dict[str, NoteRecord] = {}

    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.stem in SKIP_STEMS:
            continue

        text = path.read_text(encoding="utf-8")
        _, inner, _ = split_frontmatter(text)
        if not inner:
            continue

        slug = parse_scalar(inner, "slug") or path.stem
        title = parse_scalar(inner, "title") or slug.replace("-", " ").title()
        record = NoteRecord(
            path=path,
            slug=slug,
            title=title,
            description=parse_scalar(inner, "description"),
            tags=parse_yaml_list(inner, "tags"),
            note_kind=parse_scalar(inner, "note_kind") or "note",
            draft=parse_bool(inner, "draft"),
            utility=is_utility(inner),
            timestamp=note_timestamp(inner, path),
            resource=f"{base_url}notes/{slug}/",
        )
        records.append(record)

        keys = {title, slug, path.stem}
        keys.update(parse_yaml_list(inner, "aliases"))
        for key in keys:
            if key:
                by_key[key.casefold()] = record

    return records, by_key


def okf_link_path(record: NoteRecord) -> str:
    if record.note_kind == "index":
        return f"/hubs/{record.slug}/index.md"
    return f"/concepts/{record.slug}.md"


def resolve_target(target: str, by_key: dict[str, NoteRecord]) -> NoteRecord | None:
    return by_key.get(target.strip().casefold())


def protect_code_regions(body: str) -> tuple[str, list[tuple[str, str]]]:
    replacements: list[tuple[str, str]] = []
    counter = 0

    def shield(match: re.Match[str]) -> str:
        nonlocal counter
        token = f"@@OKF{counter}@@"
        replacements.append((token, match.group(0)))
        counter += 1
        return token

    protected = body
    for pattern in (r"```[\s\S]*?```", r"`[^`\n]+`"):
        protected = re.sub(pattern, shield, protected)
    return protected, replacements


def restore_code_regions(body: str, replacements: list[tuple[str, str]]) -> str:
    for token, original in reversed(replacements):
        body = body.replace(token, original)
    return body


def rewrite_wikilinks(body: str, by_key: dict[str, NoteRecord], base_url: str) -> str:
    protected, replacements = protect_code_regions(body)

    def repl(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        anchor = (match.group(2) or "").strip()
        suffix = f"#{anchor}" if anchor else ""
        hit = resolve_target(target, by_key)
        if hit and hit.utility:
            return f"[{hit.title}]({hit.resource})"
        if hit:
            return f"[{hit.title}]({okf_link_path(hit)}{suffix})"
        if " " in target or (target[:1].isupper() if target else False):
            return f"[{target}](/concepts/{slugify(target)}.md{suffix})"
        return match.group(0)

    rewritten = WIKILINK_RE.sub(repl, protected)
    return restore_code_regions(rewritten, replacements)


def yaml_frontmatter(fields: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if value is None or value == "":
            continue
        if isinstance(value, list):
            if not value:
                continue
            quoted = ", ".join(f'"{item}"' for item in value)
            lines.append(f"{key}: [{quoted}]")
        else:
            text = str(value)
            if re.search(r'[:#\[\]{}&,*!|>\'"%@`]', text):
                lines.append(f'{key}: "{text}"')
            else:
                lines.append(f"{key}: {text}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def write_concept(record: NoteRecord, body: str, out_dir: Path) -> None:
    dest = out_dir / "concepts" / f"{record.slug}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml_frontmatter(
        {
            "type": "Concept",
            "title": record.title,
            "description": record.description,
            "resource": record.resource,
            "tags": record.tags,
            "timestamp": record.timestamp,
        }
    )
    dest.write_text(fm + body, encoding="utf-8")


def write_hub_index(record: NoteRecord, body: str, out_dir: Path) -> None:
    dest = out_dir / "hubs" / record.slug / "index.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8")


def write_root_index(records: list[NoteRecord], out_dir: Path) -> None:
    concepts = sorted(
        (r for r in records if not r.draft and not r.utility and r.note_kind != "index"),
        key=lambda r: r.title.casefold(),
    )
    hubs = sorted(
        (r for r in records if not r.draft and not r.utility and r.note_kind == "index"),
        key=lambda r: r.title.casefold(),
    )

    lines = [
        "---",
        f'okf_version: "{OKF_VERSION}"',
        "---",
        "",
        "# JoRap Notes",
        "",
        "OKF export of the JoRap notes garden — atomic concepts and hub indexes.",
        "",
        "# Concepts",
        "",
    ]
    for record in concepts:
        desc = record.description or record.title
        lines.append(f"* [{record.title}](/concepts/{record.slug}.md) - {desc}")

    lines.extend(["", "# Hubs", ""])
    for record in hubs:
        desc = record.description or record.title
        lines.append(f"* [{record.title}](/hubs/{record.slug}/index.md) - {desc}")

    (out_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_log(out_dir: Path) -> None:
    try:
        proc = subprocess.run(
            [
                "git",
                "log",
                "--since=120 days ago",
                f"--pretty=format:%ad|%s",
                "--date=short",
                "--",
                "content/english/notes/",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        proc = None

    grouped: dict[str, list[str]] = {}
    if proc and proc.returncode == 0:
        for line in proc.stdout.splitlines():
            if "|" not in line:
                continue
            day, subject = line.split("|", 1)
            grouped.setdefault(day, []).append(subject.strip())

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ["# Directory Update Log", ""]
    if today not in grouped:
        lines.extend(
            [
                f"## {today}",
                "* **Export**: Generated OKF v0.1 bundle from the Hugo notes garden.",
                "",
            ]
        )

    for day in sorted(grouped.keys(), reverse=True):
        lines.append(f"## {day}")
        if day == today:
            lines.append("* **Export**: Generated OKF v0.1 bundle from the Hugo notes garden.")
        for subject in grouped[day][:12]:
            lines.append(f"* **Update**: {subject}")
        lines.append("")

    (out_dir / "log.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def validate_bundle(out_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(out_dir.rglob("*.md")):
        rel = path.relative_to(out_dir).as_posix()
        text = path.read_text(encoding="utf-8")

        if rel == "index.md":
            if not text.startswith("---"):
                errors.append(f"{rel}: bundle root index.md must have frontmatter with okf_version")
                continue
            if 'okf_version: "0.1"' not in text and "okf_version: '0.1'" not in text:
                errors.append(f"{rel}: missing okf_version: \"0.1\"")
            continue

        if rel == "log.md" or rel.endswith("/index.md"):
            if text.startswith("---"):
                errors.append(f"{rel}: OKF index/log files must not use concept frontmatter")
            continue

        _, inner, _ = split_frontmatter(text)
        if not inner:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        if not parse_scalar(inner, "type"):
            errors.append(f"{rel}: missing required type field")

    return errors


def export_bundle(out_dir: Path) -> tuple[int, int]:
    base_url = read_base_url()
    records, by_key = load_notes(base_url)

    if out_dir.exists():
        for path in sorted(out_dir.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
        for path in sorted(out_dir.rglob("*"), reverse=True):
            if path.is_dir():
                path.rmdir()
    out_dir.mkdir(parents=True, exist_ok=True)

    concept_count = 0
    hub_count = 0

    for record in records:
        if record.draft or record.utility:
            continue

        text = record.path.read_text(encoding="utf-8")
        _, inner, body = split_frontmatter(text)
        fm = parse_display_fields(inner)
        body = body_without_see_also(assemble_markdown(fm, body))
        body = rewrite_wikilinks(body, by_key, base_url)

        if record.note_kind == "index":
            write_hub_index(record, body, out_dir)
            hub_count += 1
        else:
            write_concept(record, body, out_dir)
            concept_count += 1

    write_root_index(records, out_dir)
    write_log(out_dir)

    viz_stats = generate_okf_viz(out_dir)
    return concept_count, hub_count, viz_stats


def generate_okf_viz(out_dir: Path) -> dict[str, int]:
    script = ROOT / "scripts/okf-viz/generate.py"
    out_path = out_dir / "viz.html"
    proc = subprocess.run(
        [sys.executable, str(script), str(out_dir), "-o", str(out_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        raise RuntimeError("OKF viz generation failed")
    match = re.search(
        r"Wrote (\d+) concept\(s\), (\d+) edge\(s\), (\d+) bytes",
        proc.stdout,
    )
    if match:
        return {
            "concepts": int(match.group(1)),
            "edges": int(match.group(2)),
            "bytes": int(match.group(3)),
        }
    return {"concepts": 0, "edges": 0, "bytes": 0}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export JoRap notes garden as an OKF v0.1 bundle.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output directory (default: {DEFAULT_OUT.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate an existing bundle without exporting.",
    )
    args = parser.parse_args()

    if args.validate_only:
        errors = validate_bundle(args.output)
        if errors:
            for err in errors:
                print(f"OKF validation error: {err}", file=sys.stderr)
            sys.exit(1)
        print(f"OKF bundle valid: {args.output}")
        return

    concepts, hubs, viz_stats = export_bundle(args.output)
    errors = validate_bundle(args.output)
    if errors:
        for err in errors:
            print(f"OKF validation error: {err}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Wrote OKF bundle to {args.output} ({concepts} concepts, {hubs} hubs, "
        f"{viz_stats['edges']} graph edges → viz.html)"
    )


if __name__ == "__main__":
    main()
