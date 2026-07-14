"""Canonical blog post frontmatter order and YAML dump (stdlib only)."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from notes_content import yaml_quote, yaml_scalar

BLOG_FM_ORDER = (
    "title",
    "meta_title",
    "description",
    "slug",
    "date",
    "image",
    "categories",
    "author",
    "tags",
    "related_notes",
    "aliases",
    "featured",
    "draft",
    "lastmod",
)

BLOG_ALWAYS_QUOTE = frozenset(
    {"title", "meta_title", "description", "slug", "date", "image", "author", "lastmod"}
)


def default_slug(path: Path) -> str:
    stem = path.stem
    return stem[2:] if stem.startswith("__") else stem


def normalize_date(value: Any) -> str:
    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(value, date):
        return f"{value.isoformat()}T05:00:00Z"
    text = str(value).strip()
    if text.endswith("Z") or "+" in text:
        return text
    return f"{text}Z"


def blog_yaml_scalar(key: str, value: Any) -> str:
    if key in BLOG_ALWAYS_QUOTE and value is not None:
        return f"{key}: {yaml_quote(str(value))}"
    return yaml_scalar(key, value)


def dump_blog_frontmatter(fm: dict[str, Any]) -> str:
    lines: list[str] = []
    seen: set[str] = set()

    def emit(key: str, value: Any) -> None:
        if key in seen or value is None:
            return
        seen.add(key)
        if key in {"tags", "categories", "aliases"} and isinstance(value, list):
            if not value:
                return
            quoted = ", ".join(yaml_quote(str(item)) for item in value)
            lines.append(f"{key}: [{quoted}]")
            return
        if key == "related_notes" and isinstance(value, list):
            if not value:
                return
            lines.append("related_notes:")
            for item in value:
                lines.append(f"  - {item}")
            return
        if key == "date":
            lines.append(blog_yaml_scalar(key, normalize_date(value)))
            return
        if key == "lastmod":
            lines.append(blog_yaml_scalar(key, normalize_date(value)))
            return
        line = blog_yaml_scalar(key, value)
        if line:
            lines.append(line)

    for key in BLOG_FM_ORDER:
        if key in fm:
            emit(key, fm[key])
    for key in sorted(fm):
        if key not in seen:
            emit(key, fm[key])
    return "\n".join(lines)


def canonical_blog_fm(fm: dict[str, Any], path: Path) -> dict[str, Any]:
    out = dict(fm)
    if not out.get("slug"):
        out["slug"] = default_slug(path)
    if out.get("author") != "JoRap":
        out["author"] = "JoRap"
    if "date" in out:
        out["date"] = normalize_date(out["date"])
    if "lastmod" in out:
        out["lastmod"] = normalize_date(out["lastmod"])
    if isinstance(out.get("image"), str) and not out["image"].startswith("/"):
        out["image"] = f"/{out['image'].lstrip('/')}"
    return out


def ordered_keys(fm: dict[str, Any]) -> list[str]:
    keys = list(fm.keys())
    expected = [k for k in BLOG_FM_ORDER if k in fm]
    if keys == expected:
        return keys
    return keys


def _self_check() -> None:
    sample = {
        "title": "Test",
        "meta_title": "Test",
        "description": "A post.",
        "slug": "test",
        "date": "2026-01-01T05:00:00Z",
        "image": "/images/x.jpg",
        "categories": ["Tips"],
        "author": "JoRap",
        "tags": ["A"],
        "related_notes": ["capture"],
        "featured": False,
        "draft": True,
    }
    text = dump_blog_frontmatter(sample)
    assert 'slug: "test"' in text
    assert "related_notes:\n  - capture" in text
    assert normalize_date("2026-05-03T23:00:00") == "2026-05-03T23:00:00Z"


if __name__ == "__main__":
    _self_check()
    print("blog_frontmatter self-check OK")
