#!/usr/bin/env python3
"""Prepend Jesus NASB 1995 quotes to Eternal Principles spine notes missing them."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "content" / "english" / "notes"

# slug -> (quote, ref) inserted as first line of key_concept if ref not already present
JESUS_OPENERS: dict[str, tuple[str, str]] = {
    "grace": (
        "For God so loved the world, that He gave His only begotten Son, that whoever believes in Him shall not perish, but have eternal life.",
        "John 3:16",
    ),
    "free-grace": (
        "Truly, truly, I say to you, he who hears My word, and believes Him who sent Me, has eternal life, and does not come into judgment, but has passed out of death into life.",
        "John 5:24",
    ),
    "justification": (
        "I tell you, this man went to his house justified rather than the other; for everyone who exalts himself will be humbled, but he who humbles himself will be exalted.",
        "Luke 18:14",
    ),
    "sanctification": (
        "Sanctify them in the truth; Your word is truth.",
        "John 17:17",
    ),
    "present-a-living-sacrifice": (
        "If anyone wishes to come after Me, he must deny himself, and take up his cross and follow Me.",
        "Matthew 16:24",
    ),
    "renewed-mind": (
        "If you continue in My word, then you are truly disciples of Mine; and you will know the truth, and the truth will make you free.",
        "John 8:31-32",
    ),
    "dont-copy-the-pattern": (
        "If you were of the world, the world would love its own; but because you are not of the world, but I chose you out of the world, because of this the world hates you.",
        "John 15:19",
    ),
    "discern-his-will-daily": (
        "If anyone is willing to do His will, he will know of the teaching, whether it is of God or whether I speak from Myself.",
        "John 7:17",
    ),
    "christlikeness": (
        "A pupil is not above his teacher; but everyone, after he has been fully trained, will be like his teacher.",
        "Luke 6:40",
    ),
    "faith-and-works": (
        "everyone who hears these words of Mine and acts on them, may be compared to a wise man who built his house on the rock.",
        "Matthew 7:24-27",
    ),
    "repent-and-believe": (
        "The time is fulfilled, and the kingdom of God is at hand; repent and believe in the gospel.",
        "Mark 1:15",
    ),
    "childlike-faith": (
        "Truly I say to you, whoever does not receive the kingdom of God like a child will not enter it at all.",
        "Mark 10:15",
    ),
    "judgment-seat": (
        "For the Son of Man is going to come in the glory of His Father with His angels, and WILL THEN REPAY EVERY MAN ACCORDING TO HIS DEEDS.",
        "Matthew 16:27",
    ),
    "loss-of-reward": (
        "For to everyone who has, more shall be given, and he will have an abundance; but from the one who does not have, even what he does have shall be taken away.",
        "Matthew 25:29",
    ),
    "standing-vs-fellowship": (
        "I give eternal life to them, and they will never perish; and no one will snatch them out of My hand.",
        "John 10:28",
    ),
    "assurance": (
        "Truly, truly, I say to you, he who believes has eternal life.",
        "John 6:47",
    ),
    "grateful-obedience": (
        "If you love Me, you will keep My commandments.",
        "John 14:15",
    ),
    "success-is-stewardship": (
        "Well done, good and faithful slave. You were faithful with a few things, I will put you in charge of many things; enter into the joy of your master.",
        "Matthew 25:21",
    ),
    "by-their-fruits": (
        "You will know them by their fruits.",
        "Matthew 7:16",
    ),
    "god-centered-design": (
        "Let your light shine before men in such a way that they may see your good works, and glorify your Father who is in heaven.",
        "Matthew 5:16",
    ),
    "fruits-of-the-spirit": (
        "My Father is glorified by this, that you bear much fruit, and so prove to be My disciples.",
        "John 15:8",
    ),
    "discipleship": (
        "If anyone wishes to come after Me, he must deny himself, and take up his cross daily and follow Me.",
        "Luke 9:23",
    ),
    "discipleship-vs-leadership": (
        "whoever wishes to become great among you shall be your servant, and whoever wishes to be first among you shall be your slave; just as the Son of Man did not come to be served, but to serve, and to give His life a ransom for many.",
        "Matthew 20:26-28",
    ),
    "take-up-your-cross": (
        "If anyone wishes to come after Me, he must deny himself, and take up his cross daily and follow Me.",
        "Luke 9:23",
    ),
    "christianity-and-politics": (
        "Render to Caesar the things that are Caesar's; and to God the things that are God's.",
        "Matthew 22:21",
    ),
}


def has_jesus_quote(text: str, quote: str, ref: str) -> bool:
    """True when the NASB quote already opens key_concept."""
    head = text[:500]
    return quote[:48] in head or f"{quote} ({ref})" in head


def prepend_quote(path: Path, quote: str, ref: str) -> bool:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"(key_concept: \|\n)(  )", text)
    if not m:
        return False
    kc_start = m.end(1)
    kc_body = text[kc_start:]
    if has_jesus_quote(kc_body[:800], quote, ref):
        return False
    line = f"  {quote} ({ref}).\n\n"
    new_text = text[:kc_start] + line + kc_body
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for slug, (quote, ref) in JESUS_OPENERS.items():
        path = NOTES / f"{slug}.md"
        if not path.exists():
            print(f"skip missing {slug}")
            continue
        if prepend_quote(path, quote, ref):
            print(f"updated {slug}")
            changed += 1
    # ponytail: spot-check — every opener file cites its ref in key_concept
    for slug, (_, ref) in JESUS_OPENERS.items():
        path = NOTES / f"{slug}.md"
        if path.exists():
            assert ref in path.read_text(encoding="utf-8"), slug
    print(f"Done — {changed} note(s) updated")


if __name__ == "__main__":
    main()
