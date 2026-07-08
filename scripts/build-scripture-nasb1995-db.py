#!/usr/bin/env python3
"""Build data/scripture-nasb1995.json — complete NASB 1995 Bible (jburson/bible-data).

ponytail: JSON not YAML — Hugo v0.163+ rejects 31k-verse YAML (alias limit).
Same structure as data/jesus-words.yaml; hugo.Data key stays scripture-nasb1995.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "scripture-nasb1995.json"
CACHE = ROOT / ".cache" / "scripture-nasb1995"
NASB_JSON_URL = "https://raw.githubusercontent.com/jburson/bible-data/master/data/nasb/nasb.json"

# Canonical Protestant order (matches jburson/bible-data book names).
BOOKS: list[str] = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation",
]


def smart_join(parts: list[str]) -> str:
    out = ""
    for part in parts:
        if not part:
            continue
        if (
            out
            and not out[-1].isspace()
            and not part[0].isspace()
            and out[-1] not in "([{\"'"
            and part[0] not in ".,;:!?)]}\"'"
        ):
            out += " "
        out += part
    return re.sub(r"\s+", " ", out).strip()


def parse_nasb_markup(text: str) -> tuple[str, str]:
    """jburson/bible-data: word features after * (r = red letter, p = paragraph)."""
    full_parts: list[str] = []
    wj_parts: list[str] = []
    for token in re.findall(r"\S+", text):
        plain = re.sub(r"\*[a-z]+$", "", token)
        if plain:
            full_parts.append(plain)
            if re.search(r"\*[a-z]*r[a-z]*$", token):
                wj_parts.append(plain)
    full = smart_join(full_parts)
    words = smart_join(wj_parts)
    return full, words


def ensure_nasb_json() -> Path:
    dest = CACHE / "nasb.json"
    marker = CACHE / "nasb.ok"
    if marker.exists() and dest.exists():
        return dest
    CACHE.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(NASB_JSON_URL, dest)
    marker.write_text("ok", encoding="utf-8")
    return dest


def fetch_nasb1995() -> dict[str, dict[str, str | bool]]:
    raw = ensure_nasb_json().read_text(encoding="utf-8")
    items = json.loads(raw)
    out: dict[str, dict[str, str | bool]] = {}
    for item in items:
        ref = item.get("r", "")
        if not ref.startswith("nasb:") or item.get("h"):
            continue
        _, book, ch, vs = ref.split(":", 3)
        if vs == "0" or book not in BOOKS:
            continue
        full, words = parse_nasb_markup(item.get("t", ""))
        if not full:
            continue
        out[f"{book} {ch}:{vs}"] = {
            "verse": full,
            "words": words,
            "full": bool(words) and full == words,
        }
    return out


def ref_sort_key(ref: str) -> tuple:
    book, ch, vs = parse_ref(ref)
    return BOOKS.index(book), ch, vs


def parse_ref(ref: str) -> tuple[str, int, int]:
    m = re.match(r"^(.+?) (\d+):(\d+)$", ref)
    if not m:
        raise ValueError(f"bad ref: {ref!r}")
    return m.group(1), int(m.group(2)), int(m.group(3))


def main() -> None:
    nasb = fetch_nasb1995()
    verses = {ref: {"nasb1995": nasb[ref]} for ref in sorted(nasb, key=ref_sort_key)}

    payload = {
        "meta": {
            "scope": BOOKS,
            "translations": {
                "nasb1995": {
                    "name": "New American Standard Bible (1995)",
                    "source": "jburson/bible-data (NASB, *r red-letter markers)",
                    "red_letter": "r",
                    "license": "© Lockman Foundation — site quotes only",
                },
            },
            "verse_count": len(verses),
            "nasb1995_verses": len(nasb),
        },
        "verses": verses,
    }

    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} — {len(verses)} verses")

    # ponytail: spot-check Genesis 1:1, John 3:16 red letter, Matthew 5:3
    assert "In the beginning God created" in verses["Genesis 1:1"]["nasb1995"]["verse"]
    assert verses["Genesis 1:1"]["nasb1995"]["full"] is False
    j316 = verses["John 3:16"]["nasb1995"]
    assert "For God so loved the world" in j316["verse"]
    assert j316["words"]
    assert j316["full"] is True
    m53 = verses["Matthew 5:3"]["nasb1995"]
    assert "Blessed are the poor in spirit" in m53["verse"]
    assert m53["full"] is True


if __name__ == "__main__":
    main()
