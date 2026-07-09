#!/usr/bin/env python3
"""Build data/jesus-words.yaml — Jesus' words (red letter) in KJV, BSB, and NASB1995, Gospels + Acts."""
from __future__ import annotations

import json
import re
import urllib.request
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "jesus-words.yaml"
CACHE = ROOT / ".cache" / "jesus-words"
BSB_ZIP_URL = "https://github.com/BSB-publishing/bsb2usfm/releases/latest/download/BSB_usj.zip"
KJV_API = "https://bible.helloao.org/api/eng_kjv"
NASB_JSON_URL = "https://raw.githubusercontent.com/jburson/bible-data/master/data/nasb/nasb.json"

BOOKS: dict[str, tuple[str, int]] = {
    "Matthew": ("MAT", 28),
    "Mark": ("MRK", 16),
    "Luke": ("LUK", 24),
    "John": ("JHN", 21),
    "Acts": ("ACT", 28),
}


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.loads(resp.read())


def ensure_bsb_usj() -> Path:
    dest = CACHE / "bsb-usj"
    marker = dest / ".ok"
    if marker.exists():
        return dest
    dest.mkdir(parents=True, exist_ok=True)
    zip_path = CACHE / "BSB_usj.zip"
    CACHE.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(BSB_ZIP_URL, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)
    marker.write_text("ok", encoding="utf-8")
    return dest


def parse_bsb_usj(usj_dir: Path) -> dict[str, dict[str, str]]:
    """Walk USJ; verse markers can appear inside wj spans (e.g. Matthew 3:15)."""
    out: dict[str, dict[str, str]] = {}

    for book, (code, _) in BOOKS.items():
        data = json.loads((usj_dir / f"{code}.usj").read_text(encoding="utf-8"))
        chapter = 0
        verse = 0
        full_by_ref: dict[str, list[str]] = {}
        wj_by_ref: dict[str, list[str]] = {}

        def ref() -> str:
            return f"{book} {chapter}:{verse}"

        def add_text(text: str, *, jesus: bool) -> None:
            if not text or not verse:
                return
            full_by_ref.setdefault(ref(), []).append(text)
            if jesus:
                wj_by_ref.setdefault(ref(), []).append(text)

        def walk(node, *, jesus: bool = False) -> None:
            nonlocal chapter, verse
            if isinstance(node, dict):
                t = node.get("type")
                if t == "chapter":
                    chapter = int(node["number"])
                    verse = 0
                elif t == "verse":
                    verse = int(node["number"])
                elif t == "char" and node.get("marker") == "wj":
                    for child in node.get("content", []):
                        walk(child, jesus=True)
                    return
                elif t == "note":
                    return
                for child in node.get("content", []):
                    walk(child, jesus=jesus)
            elif isinstance(node, list):
                for child in node:
                    walk(child, jesus=jesus)
            elif isinstance(node, str):
                add_text(node, jesus=jesus)

        walk(data["content"])

        for r, parts in wj_by_ref.items():
            full = smart_join(full_by_ref.get(r, parts))
            words = smart_join(parts)
            if not words:
                continue
            out[r] = {"verse": full, "words": words, "full": full == words}

    return out


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


def extract_kjv_content(content: list) -> tuple[str, str]:
    full_parts: list[str] = []
    wj_parts: list[str] = []
    for part in content:
        if isinstance(part, str):
            full_parts.append(part)
        elif isinstance(part, dict):
            text = part.get("text", "")
            if text:
                full_parts.append(text)
                if part.get("wordsOfJesus"):
                    wj_parts.append(text)
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


def parse_nasb_markup(text: str) -> tuple[str, str]:
    """jburson/bible-data: word features after * (r = red letter)."""
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


def fetch_nasb1995() -> dict[str, dict[str, str]]:
    raw = ensure_nasb_json().read_text(encoding="utf-8")
    items = json.loads(raw) if raw.lstrip().startswith("[") else [
        json.loads(line) for line in raw.splitlines() if line.strip()
    ]
    out: dict[str, dict[str, str]] = {}
    for item in items:
        ref = item.get("r", "")
        if not ref.startswith("nasb:"):
            continue
        _, book, ch, vs = ref.split(":", 3)
        if book not in BOOKS:
            continue
        full, words = parse_nasb_markup(item.get("t", ""))
        if not words:
            continue
        out[f"{book} {ch}:{vs}"] = {
            "verse": full,
            "words": words,
            "full": full == words,
        }
    return out


def fetch_kjv() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for book, (code, chapters) in BOOKS.items():
        for ch in range(1, chapters + 1):
            data = fetch_json(f"{KJV_API}/{code}/{ch}.json")
            for item in data["chapter"]["content"]:
                if item.get("type") != "verse":
                    continue
                full, words = extract_kjv_content(item["content"])
                if not words:
                    continue
                ref = f"{book} {ch}:{item['number']}"
                out[ref] = {
                    "verse": full,
                    "words": words,
                    "full": full == words,
                }
    return out


def merge(*translations: dict[str, dict]) -> dict[str, dict]:
    refs = sorted(set().union(*translations), key=ref_sort_key)
    keys = ("kjv", "bsb", "nasb1995")
    verses: dict[str, dict] = {}
    for ref in refs:
        entry: dict = {}
        for key, data in zip(keys, translations):
            if ref in data and data[ref]["words"]:
                entry[key] = data[ref]
        if entry:
            verses[ref] = entry
    return verses


def ref_sort_key(ref: str) -> tuple:
    book, rest = ref.split(" ", 1)
    ch, vs = rest.split(":")
    order = list(BOOKS).index(book)
    return order, int(ch), int(vs)


def main() -> None:
    usj_dir = ensure_bsb_usj()
    bsb = parse_bsb_usj(usj_dir)
    kjv = fetch_kjv()
    nasb1995 = fetch_nasb1995()
    verses = merge(kjv, bsb, nasb1995)

    payload = {
        "meta": {
            "scope": list(BOOKS),
            "translations": {
                "kjv": {
                    "name": "King James Version",
                    "source": KJV_API,
                    "red_letter": "wordsOfJesus",
                    "license": "public domain (US)",
                },
                "bsb": {
                    "name": "Berean Standard Bible",
                    "source": "BSB USJ (BSB-publishing/bsb2usfm)",
                    "red_letter": "wj",
                    "license": "public domain",
                },
                "nasb1995": {
                    "name": "New American Standard Bible (1995)",
                    "source": "jburson/bible-data (NASB, *r red-letter markers)",
                    "red_letter": "r",
                    "license": "© Lockman Foundation — site quotes only",
                },
            },
            "verse_count": len(verses),
            "kjv_verses": len(kjv),
            "bsb_verses": len(bsb),
            "nasb1995_verses": len(nasb1995),
        },
        "verses": verses,
    }

    OUT.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    print(
        f"Wrote {OUT} — {len(verses)} refs "
        f"({len(kjv)} KJV, {len(bsb)} BSB, {len(nasb1995)} NASB1995)"
    )

    # ponytail: spot-check Matthew 3:15 partial red letter in all translations
    sample = verses["Matthew 3:15"]
    assert "Suffer it to be so now" in sample["kjv"]["words"]
    assert "Let it be so now" in sample["bsb"]["words"]
    assert "Permit it at this time" in sample["nasb1995"]["words"]
    assert sample["kjv"]["full"] is False
    assert sample["bsb"]["full"] is False
    assert sample["nasb1995"]["full"] is False


if __name__ == "__main__":
    main()
